import asyncio
import logging
import os
import ssl
import pprint
from contextlib import AsyncExitStack

import coloredlogs
from asyncio_mqtt import Client

_ARG_LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
_ARG_MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
_ARG_MQTT_PORT = int(os.getenv("MQTT_PORT", 9001))
_ARG_MQTT_WS_PATH = os.getenv("MQTT_WS_PATH", "/mqtt")
_ARG_MQTT_TLS = bool(os.getenv("MQTT_TLS", ""))

_MQTT_WS_TRANSPORT = "websockets"

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

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    coloredlogs.install(level=_ARG_LOG_LEVEL)
    asyncio.run(_main())
