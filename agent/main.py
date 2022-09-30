import asyncio
import logging
import os
import pprint
import ssl
from contextlib import AsyncExitStack

import coloredlogs
import pandas as pd
from asyncio_mqtt import Client
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync

_ARG_LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
_ARG_MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
_ARG_MQTT_PORT = int(os.getenv("MQTT_PORT", 9001))
_ARG_MQTT_WS_PATH = os.getenv("MQTT_WS_PATH", "/mqtt")
_ARG_MQTT_TLS = bool(os.getenv("MQTT_TLS", ""))
_ARG_INFLUX_URL = os.getenv("INFLUX_URL", "http://influx:8086")
_ARG_INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "influx")
_ARG_INFLUX_ORG = os.getenv("INFLUX_ORG", "wot")
_ARG_INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "default-bucket")

_MQTT_WS_TRANSPORT = "websockets"
_START = "-3m"
_WINDOW_PERIOD = "10s"
_MOVING_AVG_N = 5
_ITER_SLEEP_SECS = 1.5
_MAX_COLUMNS = 12

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


async def _query_orientation(influx_client):
    query_api = influx_client.query_api()

    return await query_api.query_data_frame(
        (
            'from(bucket: "{bucket}") '
            "|> range(start: {start}) "
            '|> filter(fn: (r) => r["_measurement"] == "orientation") '
            '|> filter(fn: (r) => r["_field"] == "alpha" or r["_field"] == "beta" or r["_field"] == "gamma") '
            '|> group(columns: ["_measurement"]) '
            '|> difference(nonNegative: true, columns: ["_value"]) '
            "|> aggregateWindow(every: {window_period}, fn: sum, createEmpty: true) "
            "|> movingAverage(n: {moving_avg_n}) "
            '|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'
        ).format(
            bucket=_ARG_INFLUX_BUCKET,
            start=_START,
            window_period=_WINDOW_PERIOD,
            moving_avg_n=_MOVING_AVG_N,
        )
    )


async def _check_orientation(influx_client):
    while True:
        df = await _query_orientation(influx_client=influx_client)
        _logger.debug("Orientation DataFrame:\n%s", df)
        await asyncio.sleep(_ITER_SLEEP_SECS)


async def _query_clicks(influx_client):
    query_api = influx_client.query_api()

    return await query_api.query_data_frame(
        (
            'from(bucket: "{bucket}") '
            "|> range(start: {start}) "
            '|> filter(fn: (r) => r["_measurement"] == "click") '
            '|> filter(fn: (r) => r["_field"] == "click") '
            '|> group(columns: ["_field"]) '
            "|> aggregateWindow(every: {window_period}, fn: sum, createEmpty: true) "
            "|> movingAverage(n: {moving_avg_n}) "
            '|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'
        ).format(
            bucket=_ARG_INFLUX_BUCKET,
            start=_START,
            window_period=_WINDOW_PERIOD,
            moving_avg_n=_MOVING_AVG_N,
        )
    )


async def _check_clicks(influx_client):
    while True:
        df = await _query_clicks(influx_client=influx_client)
        _logger.debug("Clicks DataFrame:\n%s", df)
        await asyncio.sleep(_ITER_SLEEP_SECS)


async def _query_noise(influx_client):
    query_api = influx_client.query_api()

    return await query_api.query_data_frame(
        (
            'from(bucket: "{bucket}") '
            "|> range(start: {start}) "
            '|> filter(fn: (r) => r["_measurement"] == "noise") '
            '|> filter(fn: (r) => r["_field"] == "noise") '
            '|> group(columns: ["_field"]) '
            "|> aggregateWindow(every: {window_period}, fn: sum, createEmpty: true) "
            "|> movingAverage(n: {moving_avg_n}) "
            '|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'
        ).format(
            bucket=_ARG_INFLUX_BUCKET,
            start=_START,
            window_period=_WINDOW_PERIOD,
            moving_avg_n=_MOVING_AVG_N,
        )
    )


async def _check_noise(influx_client):
    while True:
        df = await _query_noise(influx_client=influx_client)
        _logger.debug("Noise DataFrame:\n%s", df)
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

        tasks.add(asyncio.create_task(_check_orientation(influx_client=influx_client)))
        tasks.add(asyncio.create_task(_check_clicks(influx_client=influx_client)))
        tasks.add(asyncio.create_task(_check_noise(influx_client=influx_client)))

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    pd.set_option("display.max_columns", _MAX_COLUMNS)
    coloredlogs.install(level=_ARG_LOG_LEVEL)
    asyncio.run(_main())
