"""Coordinator for the LifePowr FlexiO integration."""

from __future__ import annotations

import logging
import asyncio
from datetime import datetime

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    TOPIC_AWS_BROKER,
    TOPIC_AWS_FLEET_UPDATE,
    TOPIC_DIAGNOSTICS_AWS,
    TOPIC_DIAGNOSTICS_BMS,
    TOPIC_DIAGNOSTICS_CONNECTED,
    TOPIC_DIAGNOSTICS_EVDISCOVERY,
    TOPIC_DIAGNOSTICS_INVERTER,
    TOPIC_DIAGNOSTICS_IOMANAGER,
    TOPIC_DIAGNOSTICS_MODBUS,
    TOPIC_DIAGNOSTICS_P1,
    TOPIC_FCR,
)
from .websocket import LifepowrWebSocket

_LOGGER = logging.getLogger(__name__)


class LifepowrCoordinator(DataUpdateCoordinator):
    """LifePowr coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        host: str,
    ) -> None:
        """Initialize coordinator."""

        super().__init__(
            hass,
            _LOGGER,
            name="lifepowr",
            update_interval=None,
        )

        self.host = host
        #
        # Device identifier must never change
        #
        self.device_identifier = host

        #
        # Raw topic cache
        #
        self.topics: dict = {}

        #
        # Parsed entity cache
        #
        self._cache: dict = {
            "diagnostics": {},
            "fcr": {},
            "metadata": {},
            "cloud": {},
            "emsconf": {},
            "fcr_tender": {},
        }

        self.websocket = LifepowrWebSocket(
            host,
            self._process_message,
        )

        self._task = None

    def start(self) -> None:
        """Start websocket listener."""
        _LOGGER.warning(
            "COORDINATOR START CALLED"
        )
        self._task = self.hass.async_create_task(
            self.websocket.start()
        )
        _LOGGER.warning(
            "COORDINATOR START FINISHED"
        )
        return
    async def stop(self) -> None:
        """Stop websocket."""

        import asyncio

        _LOGGER.warning(
            "LIFEPOWR STOP CALLED"
        )

        await self.websocket.stop()

        if self._task:

            self._task.cancel()

            try:
                await self._task
            except asyncio.CancelledError:
                pass

        _LOGGER.warning(
            "LIFEPOWR STOP FINISHED"
        )
    async def _process_message(
        self,
        payload: dict,
    ) -> None:
        """Process websocket message."""

        action = payload.get("action")

        #
        # Initial diagnostics scan
        #
        if (
            action == "scan"
            and payload.get("pattern") == "diagnostics/*"
        ):
            diagnostics = payload.get(
                "message",
                {}
            )

            diagnostics_key_mapping = {
                "evDiscovery": "ev_discovery",
            }

            for key, value in diagnostics.items():

                mapped_key = diagnostics_key_mapping.get(
                    key,
                    key,
                )

                self._cache["diagnostics"][
                    mapped_key
                ] = value
                #
                # Store board model from scan payload
                #
                if mapped_key == "board":
                    self._cache["metadata"][
                        "board_model"
                    ] = value.get(
                        "details",
                        ""
                    )
                #
                # Device name
                #
                if mapped_key == "configured":
                    details = value.get(
                        "details",
                        ""
                    )
                    parts = details.split(":", 1)
                    if len(parts) == 2:
                        self._cache["metadata"][
                            "device_name"
                        ] = parts[1].strip()
                    else:
                        self._cache["metadata"][
                            "device_name"
                        ] = details.strip()

                if mapped_key == "connected":

                    self._cache["metadata"][
                        "connected_status"
                    ] = value.get(
                        "details",
                        ""
                    ).strip()
                
                if mapped_key == "eastron":
                    details = value.get(
                        "details",
                        ""
                    )
                    import re
                    match = re.search(
                        r"QoS\s*=\s*(\d+)",
                        details,
                    )
                    if match:
                        self._cache["metadata"][
                            "eastron_qos"
                        ] = int(
                            match.group(1)
                        )
                if mapped_key == "ev":
                    self._cache["metadata"][
                        "ev_status"
                    ] = value.get(
                        "details",
                        ""
                    ).strip()
                if mapped_key == "ev_discovery":

                    self._cache["metadata"][
                        "ev_discovery"
                    ] = value.get(
                        "details",
                        ""
                    ).strip()

                if mapped_key == "inverter":
                    details = value.get(
                        "details",
                        ""
                    )
                    data = value.get(
                        "data",
                        {}
                    )
                    import re
                    #
                    # Inverter Status
                    #
                    status_match = re.search(
                        r"Status:\s*([^,]+)",
                        details,
                    )
                    if status_match:
                        self._cache["metadata"][
                            "inverter_status"
                        ] = status_match.group(1).strip()
                    #
                    # Inverter Meter
                    #
                    meter_match = re.search(
                        r"Meter:\s*([^,]+)",
                        details,
                    )
                    if meter_match:
                        self._cache["metadata"][
                            "inverter_meter"
                        ] = meter_match.group(1).strip()
                    #
                    # Inverter FW
                    #
                    self._cache["metadata"][
                        "inverter_fw"
                    ] = data.get(
                        "fwDetails",
                        ""
                    )    
                    #
                    # Inverter Serial
                    #
                    self._cache["metadata"][
                        "inverter_serial"
                    ] = data.get(
                        "serialNumber",
                        ""
                    )
                if mapped_key == "ioapi":

                    self._cache["metadata"][
                        "ioapi"
                    ] = value.get(
                        "details",
                        ""
                    ).strip()
                if mapped_key == "iodaemon":

                    self._cache["metadata"][
                        "iodaemon"
                    ] = value.get(
                        "details",
                        ""
                    ).strip()
                if mapped_key == "iomanager":

                    self._cache["metadata"][
                        "iomanager"
                    ] = value.get(
                        "details",
                        ""
                    ).strip()
                if mapped_key == "update":

                    self._cache["metadata"][
                        "update_status"
                    ] = value.get(
                        "details",
                        ""
                    ).strip()
                if mapped_key == "modbus":

                    details = value.get(
                        "details",
                        ""
                    )

                    import re

                    #
                    # QoS
                    #
                    qos_match = re.search(
                        r"QoS:\s*(\d+)%",
                        details,
                    )

                    if qos_match:
                        self._cache["metadata"][
                            "modbus_qos"
                        ] = int(
                            qos_match.group(1)
                        )

                    #
                    # Adapter
                    #
                    adapter_match = re.search(
                        r"Adapter:\s*(.*)$",
                        details,
                    )

                    if adapter_match:
                        self._cache["metadata"][
                            "modbus_adapter"
                        ] = adapter_match.group(1).strip()

                    #
                    # Details (strip QoS and Adapter)
                    #
                    clean_details = re.sub(
                        r",\s*QoS:.*$",
                        "",
                        details,
                    )

                    self._cache["metadata"][
                        "modbus_details"
                    ] = clean_details.strip()
                if mapped_key == "p1":

                    details = value.get(
                        "details",
                        ""
                    )

                    import re

                    #
                    # P1 Status
                    #
                    status_match = re.search(
                        r"^(.*?)\. QoS:",
                        details,
                    )

                    if status_match:
                        self._cache["metadata"][
                            "p1_status"
                        ] = status_match.group(1).strip()

                    #
                    # P1 QoS
                    #
                    qos_match = re.search(
                        r"QoS:\s*(\d+)%",
                        details,
                    )

                    if qos_match:
                        self._cache["metadata"][
                            "p1_qos"
                        ] = int(
                            qos_match.group(1)
                        )

                    #
                    # P1 Grid
                    #
                    gridtype_match = re.search(
                        r",\s*([^,]+)$",
                        details,
                    )

                    if gridtype_match:
                        self._cache["metadata"][
                            "p1_gridtype"
                        ] = gridtype_match.group(1).strip()
                if mapped_key == "storage":

                    self._cache["metadata"][
                        "storage_details"
                    ] = value.get(
                        "details",
                        ""
                    ).strip()












            self.async_set_updated_data(
                self._cache
            )
            return

        topic = payload.get("topic")

        if not topic:
            return

        message = payload.get("message")

        self.topics[topic] = message

        try:

            if topic.startswith("diagnostics/"):
                self._handle_diagnostic(
                    topic,
                    message,
                )

            elif topic == TOPIC_AWS_BROKER:
                self._cache["cloud"][
                    "aws_broker_ready"
                ] = bool(message)

            elif topic == TOPIC_FCR:
                self._handle_fcr(message)

            elif topic == TOPIC_AWS_FLEET_UPDATE:
                self._handle_fleet_update(
                    message
                )

            self._cache["last_update"] = (
                datetime.utcnow()
                .isoformat()
            )

            self.async_set_updated_data(
                self._cache
            )

        except Exception:
            _LOGGER.exception(
                "Failed processing topic %s",
                topic,
            )

    def _handle_diagnostic(
        self,
        topic: str,
        message: dict,
    ) -> None:
        """Handle diagnostics topics."""

        raw_key = topic.split("/")[-1]

        mapping = {
            "evDiscovery": "ev_discovery",
        }

        key = mapping.get(
            raw_key,
            raw_key,
        )
        diagnostic = {
            "status": message.get(
                "status",
                False,
            ),
            "details": message.get(
                "details",
                "",
            ),
        }

        #
        # Inverter metadata
        #
        if (
            topic
            == TOPIC_DIAGNOSTICS_INVERTER
        ):
            data = message.get(
                "data",
                {},
            )

            self._cache["metadata"][
                "inverter_serial"
            ] = data.get(
                "serialNumber"
            )

            self._cache["metadata"][
                "inverter_firmware"
            ] = data.get(
                "fwDetails"
            )

        #
        # AWS QoS
        #
        # if topic == TOPIC_DIAGNOSTICS_AWS:
        #     diagnostic["qos_text"] = (
        #         message.get(
        #             "details",
        #             "",
        #         )
        #     )
        if topic == TOPIC_DIAGNOSTICS_AWS:
            details = message.get(
                "details",
                "",
            )
            diagnostic["qos_text"] = details
            import re
            match = re.search(
                r"QoS:\s*(\d+)",
                details,
            )
            if match:
                self._cache["metadata"][
                    "aws_qos"
                ] = int(
                    match.group(1)
                )
        #
        # BMS status and model
        #
        if topic == TOPIC_DIAGNOSTICS_BMS:
            details = message.get(
                "details",
                ""
            )
            import re
            #
            # Status
            #
            status_match = re.search(
                r"Status:\s*([^,]+)",
                details,
            )
            if status_match:
                self._cache["metadata"][
                    "bms_status"
                ] = status_match.group(1).strip()
            #
            # Model
            #
            model_match = re.search(
                r"Model:\s*(.*)$",
                details,
            )
            if model_match:
                self._cache["metadata"][
                    "bms_model"
                ] = model_match.group(1).strip()
        #
        # P1 QoS
        #
        if topic == TOPIC_DIAGNOSTICS_P1:
            diagnostic["p1_info"] = (
                message.get(
                    "details",
                    "",
                )
            )

        self._cache["diagnostics"][
            key
        ] = diagnostic

    def _handle_fcr(
        self,
        message: dict,
    ) -> None:
        """Handle FCR updates."""

        if not message:
            return

        #
        # Actual metrics are nested inside
        # message.message
        #
        payload = message.get(
            "message",
            {}
        )

        self._cache["fcr"] = {
            "baseline": payload.get(
                "frequencyResponseBaseline"
            ),
            "measurement": payload.get(
                "frequencyResponseMeasurement"
            ),
            "error": payload.get(
                "frequencyResponseError"
            ),
            "available_margin_charge":
                payload.get(
                    "frequencyResponseAvailableMarginCharge"
                ),
            "available_margin_discharge":
                payload.get(
                    "frequencyResponseAvailableMarginDischarge"
                ),
            "charge_discharge_power":
                payload.get(
                    "frequencyResponseChargeDischargePower"
                ),
            "timestamp": payload.get(
                "timestamp"
            ),
            "stream": message.get(
                "stream"
            ),
            "global_stream": message.get(
                "globalStream"
            ),
            "bsp": message.get(
                "bsp"
            ),
            "event_id": message.get(
                "eventId"
            ),
        }

    def _handle_fleet_update(
        self,
        message: dict,
    ) -> None:
        """Handle cloud fleet updates."""

        if not message:
            return
        #
        # FCR Tender forecast
        #
        fcr_tender = message.get(
            "fcrTenderPrices",
            {}
        )

        if fcr_tender:
            self._cache["fcr_tender"] = fcr_tender
        #
        # EMS configuration
        #
        emsconf = message.get(
            "emsconf",
            {}
        )

        for key, value in emsconf.items():
            self._cache["emsconf"][key] = value
        #
        # Dynamic electricity pricing
        #
        if (
            "belpex_average"
            in message
        ):
            self._cache["cloud"][
                "belpex_average"
            ] = message[
                "belpex_average"
            ]

        prices = message.get(
            "electricityPrices"
        )

        if prices:
            self._cache["cloud"][
                "price_points"
            ] = len(
                prices.get(
                    "timestamps",
                    []
                )
            )

            self._cache["cloud"][
                "has_future_prices"
            ] = (
                len(
                    prices.get(
                        "timestamps",
                        []
                    )
                )
                > 0
            )

    #
    # Helper methods for entities
    #

    def get_diagnostic(
        self,
        key: str,
    ) -> dict:
        """Return diagnostic state."""

        return (
            self._cache
            .get(
                "diagnostics",
                {}
            )
            .get(
                key,
                {}
            )
        )

    def get_fcr(
        self,
        key: str,
    ):
        """Return FCR metric."""

        return (
            self._cache
            .get(
                "fcr",
                {}
            )
            .get(key)
        )

    def get_metadata(
        self,
        key: str,
    ):
        """Return metadata value."""

        return (
            self._cache
            .get(
                "metadata",
                {}
            )
            .get(key)
        )

    def get_cloud(
        self,
        key: str,
    ):
        """Return cloud value."""

        return (
            self._cache
            .get(
                "cloud",
                {}
            )
            .get(key)
        )

    def get_device_name(self) -> str:
        """Return display name."""

        return (
            self.get_metadata(
                "device_name"
            )
            or "LifePowr FlexiO"
        )
    def get_device_identifier(self) -> str:
        """Return stable identifier."""

        return self.device_identifier
    def get_emsconf(
        self,
        key: str,
    ):
        """Return EMS configuration value."""

        return (
            self._cache
            .get(
                "emsconf",
                {}
            )
            .get(key)
        )

    def get_fcr_tender(self):
        """Return FCR tender forecast."""

        return (
            self._cache
            .get(
                "fcr_tender",
                {}
            )
        )