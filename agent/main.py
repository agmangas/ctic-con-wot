import asyncio
import json
import logging
import os
import pprint
import ssl
import warnings
from contextlib import AsyncExitStack

import coloredlogs
from asyncio_mqtt import Client
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from influxdb_client.client.warnings import MissingPivotFunction

warnings.simplefilter("ignore", MissingPivotFunction)

_MQTT_WS_TRANSPORT = "websockets"
_START = "-2m"
_WINDOW_PERIOD = "10s"
_ITER_SLEEP_SECS = 1.5
_TOPIC_CURRENT_STATS = "sensors-app/aggregated-stats"
_TOPIC_ALERT = "sensors-app/alert"
_TOPIC_SLIDES_COMMAND = "slides/command"
_KEY_ORIENTATION = "orientation"
_KEY_CLICKS = "clicks"
_KEY_NOISE = "noise"
_KEY_ALERT_ACTIVE = "active"
_KEY_ALERT_CURRENT = "current"
_KEY_ALERT_TARGET = "target"
_ENV_NEXT_SLIDE_SENSORS = "SENSORS_NEXT_SLIDE"
_ENV_NEXT_SLIDE_BUTTON = "BUTTON_NEXT_SLIDE"
_ENV_NEXT_SLIDE_TEMPERATURE = "TEMPERATURE_NEXT_SLIDE"

_ARG_LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
_ARG_MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
_ARG_MQTT_PORT = int(os.getenv("MQTT_PORT", 9001))
_ARG_MQTT_WS_PATH = os.getenv("MQTT_WS_PATH", "/mqtt")
_ARG_MQTT_TLS = bool(os.getenv("MQTT_TLS", ""))
_ARG_INFLUX_URL = os.getenv("INFLUX_URL", "http://influx:8086")
_ARG_INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "influx")
_ARG_INFLUX_ORG = os.getenv("INFLUX_ORG", "wot")
_ARG_INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "default-bucket")
_ARG_TARGET_AVG_ORIENTATION_DIFF = float(os.getenv("TARGET_AVG_ORIENTATION_DIFF", 4000))
_ARG_TARGET_AVG_CLICKS = float(os.getenv("TARGET_AVG_CLICKS", 35))
_ARG_TARGET_AVG_NOISE = float(os.getenv("TARGET_AVG_NOISE", 1.0))
_ARG_TARGET_NUM_CLIENTS = float(os.getenv("TARGET_NUM_CLIENTS", 8))

_ARG_NEXT_SLIDE_SENSORS = (
    int(os.getenv(_ENV_NEXT_SLIDE_SENSORS))
    if os.getenv(_ENV_NEXT_SLIDE_SENSORS)
    else None
)

_ARG_NEXT_SLIDE_BUTTON = (
    int(os.getenv(_ENV_NEXT_SLIDE_BUTTON))
    if os.getenv(_ENV_NEXT_SLIDE_BUTTON)
    else None
)

_ARG_NEXT_SLIDE_TEMPERATURE = (
    int(os.getenv(_ENV_NEXT_SLIDE_TEMPERATURE))
    if os.getenv(_ENV_NEXT_SLIDE_TEMPERATURE)
    else None
)


_logger = logging.getLogger(__name__)


async def _cancel_tasks(tasks):
    for task in tasks:
        if task.done():
            continue
        try:
            _logger.debug("Cancelling task: %s", task)
            task.cancel()
            await task
        except asyncio.CancelledError:
            pass


async def _query_distinct_clients(influx_client, start="-1m"):
    query_api = influx_client.query_api()

    return await query_api.query_data_frame(
        (
            'from(bucket: "{bucket}") '
            "|> range(start: {start}) "
            '|> filter(fn: (r) => r["_measurement"] == "noise" or r["_measurement"] == "click") '
            '|> group(columns: ["device"]) '
            '|> distinct(column: "device")'
        ).format(bucket=_ARG_INFLUX_BUCKET, start=start)
    )


async def _query_orientation(influx_client):
    query_api = influx_client.query_api()

    df = await query_api.query_data_frame(
        (
            'from(bucket: "{bucket}") '
            "|> range(start: {start}) "
            '|> filter(fn: (r) => r["_measurement"] == "orientation") '
            '|> filter(fn: (r) => r["_field"] == "alpha" or r["_field"] == "beta" or r["_field"] == "gamma") '
            '|> group(columns: ["_measurement"]) '
            '|> difference(nonNegative: true, columns: ["_value"]) '
            "|> aggregateWindow(every: {window_period}, fn: sum, createEmpty: true) "
        ).format(
            bucket=_ARG_INFLUX_BUCKET,
            start=_START,
            window_period=_WINDOW_PERIOD,
        )
    )

    return df.fillna(0)


async def _query_clicks(influx_client):
    query_api = influx_client.query_api()

    df = await query_api.query_data_frame(
        (
            'from(bucket: "{bucket}") '
            "|> range(start: {start}) "
            '|> filter(fn: (r) => r["_measurement"] == "click") '
            '|> filter(fn: (r) => r["_field"] == "click") '
            '|> group(columns: ["_field"]) '
            "|> aggregateWindow(every: {window_period}, fn: sum, createEmpty: true) "
        ).format(
            bucket=_ARG_INFLUX_BUCKET,
            start=_START,
            window_period=_WINDOW_PERIOD,
        )
    )

    return df.fillna(0)


async def _query_noise(influx_client):
    query_api = influx_client.query_api()

    df = await query_api.query_data_frame(
        (
            'from(bucket: "{bucket}") '
            "|> range(start: {start}) "
            '|> filter(fn: (r) => r["_measurement"] == "noise") '
            '|> filter(fn: (r) => r["_field"] == "noise") '
            '|> group(columns: ["device"]) '
            "|> aggregateWindow(every: {window_period}, fn: mean, createEmpty: true) "
            '|> group(columns: ["_field"]) '
            "|> aggregateWindow(every: {window_period}, fn: sum, createEmpty: true) "
        ).format(
            bucket=_ARG_INFLUX_BUCKET,
            start=_START,
            window_period=_WINDOW_PERIOD,
        )
    )

    return df.fillna(0)


def _get_df_stats(df, round_len=3, key_time="_time", key_value="_value"):
    if df.empty:
        return None

    df_sorted = df.sort_values(by=[key_time])
    ser_values = df_sorted[key_value]

    stats = {
        key: round(val, round_len)
        for key, val in ser_values.describe().to_dict().items()
    }

    stats.update(
        {
            "sum": round(ser_values.sum(), round_len),
            "values": ser_values.round(round_len).astype("float").to_list(),
        }
    )

    return stats


def _get_alert_body(df, target, round_len=3, key_value="_value"):
    curr_max = df[key_value].max() if not df.empty else None

    return {
        _KEY_ALERT_ACTIVE: bool(curr_max >= target) if curr_max is not None else False,
        _KEY_ALERT_CURRENT: round(curr_max, round_len)
        if curr_max is not None
        else None,
        _KEY_ALERT_TARGET: round(target, round_len),
    }


async def _next_slide(mqtt_client, slide_idx, qos=2):
    payload = {"method": "slide", "args": [slide_idx]}
    _logger.info("Publishing to '%s': %s", _TOPIC_SLIDES_COMMAND, payload)
    await mqtt_client.publish(_TOPIC_SLIDES_COMMAND, json.dumps(payload), qos=qos)


async def _check_sensors(influx_client, mqtt_client, stats_qos=0, alert_qos=2):
    while True:
        df_orientation = await _query_orientation(influx_client=influx_client)
        _logger.debug("Orientation DataFrame:\n%s", df_orientation)

        df_clicks = await _query_clicks(influx_client=influx_client)
        _logger.debug("Clicks DataFrame:\n%s", df_clicks)

        df_noise = await _query_noise(influx_client=influx_client)
        _logger.debug("Noise DataFrame:\n%s", df_noise)

        df_clients = await _query_distinct_clients(influx_client=influx_client)
        _logger.debug("Clients DataFrame:\n%s", df_clients)

        stats_noise = _get_df_stats(df_noise)
        stats_click = _get_df_stats(df_clicks)
        stats_orientation = _get_df_stats(df_orientation)

        curr_stats = {
            _KEY_NOISE: stats_noise,
            _KEY_CLICKS: stats_click,
            _KEY_ORIENTATION: stats_orientation,
            "num_clients": df_clients.shape[0],
        }

        _logger.info("Current stats:\n%s", pprint.pformat(curr_stats))

        await mqtt_client.publish(
            _TOPIC_CURRENT_STATS, json.dumps(curr_stats), qos=stats_qos
        )

        target_orient = _ARG_TARGET_AVG_ORIENTATION_DIFF * _ARG_TARGET_NUM_CLIENTS
        target_noise = _ARG_TARGET_AVG_NOISE * _ARG_TARGET_NUM_CLIENTS
        target_clicks = _ARG_TARGET_AVG_CLICKS * _ARG_TARGET_NUM_CLIENTS

        alert_body = {
            _KEY_ORIENTATION: _get_alert_body(df=df_orientation, target=target_orient),
            _KEY_NOISE: _get_alert_body(df=df_noise, target=target_noise),
            _KEY_CLICKS: _get_alert_body(df=df_clicks, target=target_clicks),
        }

        _logger.info("Alert:\n%s", alert_body)

        await mqtt_client.publish(_TOPIC_ALERT, json.dumps(alert_body), qos=alert_qos)

        all_alerts_active = all(
            [item[_KEY_ALERT_ACTIVE] for item in alert_body.values()]
        )

        _logger.log(
            logging.INFO if all_alerts_active else logging.DEBUG,
            "All alerts active: %s",
            all_alerts_active,
        )

        if all_alerts_active and _ARG_NEXT_SLIDE_SENSORS is not None:
            await _next_slide(
                mqtt_client=mqtt_client, slide_idx=_ARG_NEXT_SLIDE_SENSORS
            )

        await asyncio.sleep(_ITER_SLEEP_SECS)


async def _check_button(influx_client, mqtt_client, start="-40s"):
    while True:
        query_api = influx_client.query_api()

        df = await query_api.query_data_frame(
            (
                'from(bucket: "{bucket}") '
                "|> range(start: {start}) "
                '|> filter(fn: (r) => r["_measurement"] == "button") '
                "|> limit(n: 1)"
            ).format(
                bucket=_ARG_INFLUX_BUCKET,
                start=start,
            )
        )

        _logger.debug("Button DataFrame:\n%s", df)

        if not df.empty and _ARG_NEXT_SLIDE_BUTTON is not None:
            await _next_slide(mqtt_client=mqtt_client, slide_idx=_ARG_NEXT_SLIDE_BUTTON)

        await asyncio.sleep(_ITER_SLEEP_SECS)


async def _check_temperature(influx_client, mqtt_client, start="-40s", threshold=40):
    while True:
        query_api = influx_client.query_api()

        df = await query_api.query_data_frame(
            (
                'from(bucket: "{bucket}") '
                "|> range(start: {start}) "
                '|> filter(fn: (r) => r["_measurement"] == "temperature") '
                '|> filter(fn: (r) => r["_field"] == "value") '
            ).format(bucket=_ARG_INFLUX_BUCKET, start=start, threshold=threshold)
        )

        df = df[df._value >= threshold]

        _logger.debug("Temperature DataFrame:\n%s", df)

        if not df.empty and _ARG_NEXT_SLIDE_TEMPERATURE is not None:
            await _next_slide(
                mqtt_client=mqtt_client, slide_idx=_ARG_NEXT_SLIDE_TEMPERATURE
            )

        await asyncio.sleep(_ITER_SLEEP_SECS)


async def _main():
    async with AsyncExitStack() as stack:
        tasks = set()
        stack.push_async_callback(_cancel_tasks, tasks)

        mqtt_client_kwargs = {
            "hostname": _ARG_MQTT_HOST,
            "port": _ARG_MQTT_PORT,
            "transport": _MQTT_WS_TRANSPORT,
            "websocket_path": _ARG_MQTT_WS_PATH,
            "websocket_headers": {"Host": _ARG_MQTT_HOST},
            "tls_context": ssl.create_default_context() if _ARG_MQTT_TLS else None,
        }

        _logger.info(
            "Connecting to MQTT broker:\n%s", pprint.pformat(mqtt_client_kwargs)
        )

        mqtt_client = Client(**mqtt_client_kwargs)
        await stack.enter_async_context(mqtt_client)

        influx_client_kwargs = {
            "url": _ARG_INFLUX_URL,
            "token": _ARG_INFLUX_TOKEN,
            "org": _ARG_INFLUX_ORG,
        }

        _logger.info(
            "Connecting to InfluxDB:\n%s", pprint.pformat(influx_client_kwargs)
        )

        influx_client = InfluxDBClientAsync(**influx_client_kwargs)
        await stack.enter_async_context(influx_client)

        influx_ready = await influx_client.ping()
        assert influx_ready

        tasks.add(
            asyncio.create_task(
                _check_sensors(influx_client=influx_client, mqtt_client=mqtt_client)
            )
        )

        tasks.add(
            asyncio.create_task(
                _check_button(influx_client=influx_client, mqtt_client=mqtt_client)
            )
        )

        tasks.add(
            asyncio.create_task(
                _check_temperature(influx_client=influx_client, mqtt_client=mqtt_client)
            )
        )

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    coloredlogs.install(level=_ARG_LOG_LEVEL)
    asyncio.run(_main())
