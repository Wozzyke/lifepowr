"""WebSocket client for LifePowr FlexiO."""

from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import Awaitable, Callable

import aiohttp

from .const import WEBSOCKET_PATH

_LOGGER = logging.getLogger(__name__)


MessageCallback = Callable[[dict], Awaitable[None]]


class LifepowrWebSocket:
    """Manage the LifePowr websocket connection."""

    def __init__(
        self,
        host: str,
        callback: MessageCallback,
    ) -> None:
        """Initialize websocket client."""

        self._host = host
        self._callback = callback

        self._running = False
        self._session: aiohttp.ClientSession | None = None
        self._ws: aiohttp.ClientWebSocketResponse | None = None

    @property
    def websocket_url(self) -> str:
        """Return websocket URL."""

        return f"ws://{self._host}{WEBSOCKET_PATH}"

    async def start(self) -> None:
        """Start websocket reconnect loop."""

        self._running = True
        while self._running:
            try:
                await self._connect()
            except asyncio.CancelledError:
                raise
            except Exception:
                _LOGGER.exception(
                    "Unexpected websocket error"
                )

            if self._running:
                await asyncio.sleep(5)

    async def stop(self) -> None:
        """Stop websocket."""
        self._running = False
        if self._ws and not self._ws.closed:
            await self._ws.close()
        if self._session:
            await self._session.close()
    async def _connect(self) -> None:
        """Connect to LifePowr websocket."""
        async with aiohttp.ClientSession() as session:
            self._session = session
            async with session.ws_connect(
                self.websocket_url,
                heartbeat=30,
            ) as ws:
                self._ws = ws
                await self._subscribe(ws)
                while self._running:
                    try:
                        msg = await ws.receive()
                    except asyncio.CancelledError:
                        raise
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        await self._handle_text(
                            msg.data
                        )
                    elif msg.type in (
                        aiohttp.WSMsgType.CLOSED,
                        aiohttp.WSMsgType.CLOSE,
                    ):
                        break
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        break
                self._ws = None
    async def _subscribe(
        self,
        ws: aiohttp.ClientWebSocketResponse,
    ) -> None:
        """Subscribe to telemetry streams."""
        #
        # Based on protocol discovery.
        #
        await ws.send_str("scan/diagnostics/*")
        await ws.send_str("listen/diagnostics/*")
        await ws.send_str("listen/*")
    async def _handle_text(
        self,
        raw_message: str,
    ) -> None:
        """Process websocket frame."""

        try:
            payload = json.loads(
                raw_message
            )

        except json.JSONDecodeError:

            _LOGGER.debug(
                "Ignoring invalid JSON frame"
            )

            return

        #
        # Only process JSON objects.
        #
        if not isinstance(
            payload,
            dict,
        ):

            _LOGGER.debug(
                "Ignoring non-object JSON payload: %s",
                type(payload).__name__,
            )

            return

        topic = payload.get(
            "topic"
        )

        if topic:

            _LOGGER.debug(
                "Topic received: %s",
                topic,
            )

        try:

            await self._callback(
                payload
            )

        except Exception:

            _LOGGER.exception(
                "Message callback failed"
            )
def extract_topic(payload: dict) -> str | None:
    """Return topic from payload."""

    return payload.get("topic")


def extract_message(payload: dict):
    """Return message from payload."""

    return payload.get("message")


def is_fcr_event(payload: dict) -> bool:
    """Determine whether payload is an FCR update."""

    return (
        payload.get("topic")
        == "iomanager/Publicationsq1/$aws/rules/aggregator"
    )


def is_diagnostic_event(payload: dict) -> bool:
    """Determine whether payload is a diagnostic event."""

    topic = payload.get("topic", "")

    return topic.startswith("diagnostics/")


def is_aws_broker_ready(payload: dict) -> bool:
    """Determine whether payload contains AWS broker ready state."""

    return (
        payload.get("topic")
        == "/flags/awsBrokerReady"
    )