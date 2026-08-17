"""Sensors for LifePowr FlexiO."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import (
    AddEntitiesCallback,
)
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from datetime import UTC, datetime
from .const import (
    DEVICE_FCR,
    DEVICE_METADATA,
    DOMAIN,
    FCR_SENSORS,
    MANUFACTURER,
    METADATA_SENSORS,
    MODEL,
    EMSCONF_SENSORS,
    FCR_TENDER_SENSORS,
)
from .coordinator import LifepowrCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up LifePowr sensors."""

    coordinator: LifepowrCoordinator = (
        hass.data[DOMAIN][entry.entry_id]
    )

    entities = []
    #
    # FCR Tender sensors
    #
    for definition in FCR_TENDER_SENSORS:
        entities.append(
            LifepowrFCRTenderSensor(
                coordinator,
                entry,
                definition,
            )
        )
    #
    # FCR sensors
    #
    for definition in FCR_SENSORS:
        entities.append(
            LifepowrFCRSensor(
                coordinator,
                entry,
                definition,
            )
        )

    #
    # Metadata sensors
    #
    for definition in METADATA_SENSORS:
        entities.append(
            LifepowrMetadataSensor(
                coordinator,
                entry,
                definition,
            )
        )
    #
    # EMS Configuration sensors
    #
    for definition in EMSCONF_SENSORS:
        entities.append(
            LifepowrEMSConfSensor(
                coordinator,
                entry,
                definition,
            )
        )
    async_add_entities(entities)

# ============================================================
# FCR TENDER SENSORS
# ============================================================
class LifepowrFCRTenderSensor(
    CoordinatorEntity,
    SensorEntity,
):
    """FCR Tender forecast sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator,
        entry,
        definition,
    ):
        super().__init__(coordinator)

        self._definition = definition

        self._attr_name = (
            definition["name"]
        )

        self._attr_unique_id = (
            f"lifepowr_{entry.entry_id}_"
            f"{definition['key']}"
        )

        self._attr_icon = definition.get(
            "icon"
        )

        self._attr_native_unit_of_measurement = (
            definition.get("unit")
        )
    @property
    def device_info(self) -> DeviceInfo:
        """Device information."""

        return DeviceInfo(
            identifiers={
                (
                    DOMAIN,
                    self.coordinator.get_device_identifier(),
                )
            },
            name="LifePowr FlexiO",
            manufacturer=MANUFACTURER,
            model=MODEL,
            configuration_url=f"http://{self.coordinator.host}",
        )
    @property
    def native_value(self):
        """Return current FCR price."""

        data = (
            self.coordinator.get_fcr_tender()
        )

        values = data.get(
            "values",
            []
        )

        if not values:
            return None

        return values[0]
    @property
    def extra_state_attributes(self):
        """Forecast data."""

        data = (
            self.coordinator.get_fcr_tender()
        )

        timestamps = data.get(
            "timestamps",
            []
        )

        values = data.get(
            "values",
            []
        )

        forecast = []

        for ts, value in zip(
            timestamps,
            values,
        ):
            forecast.append(
                {
                    "datetime": datetime.fromtimestamp(
                        ts,
                        UTC,
                    ).isoformat(),
                    "price": value,
                }
            )
        return {
            "forecast": forecast,
            "forecast_count": len(values),
            "current_price":
                values[0]
                if values
                else None,
            "next_price":
                values[1]
                if len(values) > 1
                else None,
            "max_price":
                max(values)
                if values
                else None,
            "max_nonzero_price":
                max(
                    v
                    for v in values
                    if v > 0
                )
                if any(
                    v > 0
                    for v in values
                )
                else None,
            "min_price":
                min(values)
                if values
                else None,
            "average_price":
                (
                    sum(values)
                    / len(values)
                )
                if values
                else None,
        }
# ============================================================
# FCR SENSORS
# ============================================================
class LifepowrFCRSensor(
    CoordinatorEntity,
    SensorEntity,
):
    """FCR telemetry sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: LifepowrCoordinator,
        entry: ConfigEntry,
        definition: dict,
    ) -> None:
        """Initialize entity."""

        super().__init__(coordinator)

        self._entry = entry
        self._definition = definition

        self._attr_name = (
            definition["name"]
        )

        self._attr_unique_id = (
            f"lifepowr_"
            f"{entry.entry_id}_"
            f"{definition['key']}"
        )

        self._attr_icon = definition.get(
            "icon"
        )

        self._attr_native_unit_of_measurement = (
            definition.get(
                "native_unit"
            )
        )


    @property
    def device_info(
        self,
    ) -> DeviceInfo:
        """Return device information."""

        return DeviceInfo(
            identifiers={
                (
                    DOMAIN,
                    self.coordinator.get_device_identifier(),
                )
            },
            name="LifePowr FlexiO",
            manufacturer=MANUFACTURER,
            model=MODEL,
            configuration_url=f"http://{self.coordinator.host}",
        )    

    @property
    def native_value(self):
        """Return sensor value."""

        field = self._definition[
            "field"
        ]

        mapped = {
            "frequencyResponseBaseline":
                "baseline",
            "frequencyResponseMeasurement":
                "measurement",
            "frequencyResponseError":
                "error",
            "frequencyResponseAvailableMarginCharge":
                "available_margin_charge",
            "frequencyResponseAvailableMarginDischarge":
                "available_margin_discharge",
            "frequencyResponseChargeDischargePower":
                "charge_discharge_power",
        }

        return self.coordinator.get_fcr(
            mapped[field]
        )

    @property
    def extra_state_attributes(
        self,
    ):
        """Extra attributes."""

        return {
            "bsp": self.coordinator.get_fcr(
                "bsp"
            ),
            "stream": self.coordinator.get_fcr(
                "stream"
            ),
            "global_stream":
                self.coordinator.get_fcr(
                    "global_stream"
                ),
            "event_id":
                self.coordinator.get_fcr(
                    "event_id"
                ),
            "timestamp":
                self.coordinator.get_fcr(
                    "timestamp"
                ),
        }
# ============================================================
# METADATA SENSORS
# ============================================================
class LifepowrMetadataSensor(
    CoordinatorEntity,
    SensorEntity,
):
    """Metadata sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: LifepowrCoordinator,
        entry: ConfigEntry,
        definition: dict,
    ) -> None:
        """Initialize sensor."""

        super().__init__(coordinator)

        self._entry = entry
        self._definition = definition

        self._attr_name = (
            definition["name"]
        )

        self._attr_unique_id = (
            f"lifepowr_"
            f"{entry.entry_id}_"
            f"{definition['key']}"
        )

        self._attr_native_unit_of_measurement = (
            definition.get("unit")
        )
        self._attr_icon = definition.get(
            "icon"
        )

    @property
    def device_info(
        self,
    ) -> DeviceInfo:
        """Device information."""

        return DeviceInfo(
            identifiers={
                (
                    DOMAIN,
                    self.coordinator.get_device_identifier(),
                )
            },
            name="LifePowr FlexiO",
            manufacturer=MANUFACTURER,
            model=MODEL,
            configuration_url=f"http://{self.coordinator.host}",
        )
    
    @property
    def native_value(self):
        """Return state."""

        key = self._definition[
            "key"
        ]

        #
        # Metadata
        #
        if key in (
            "inverter_serial",
            "inverter_firmware",
        ):
            return (
                self.coordinator.get_metadata(
                    key
                )
            )

        #
        # FCR metadata
        #
        if key == "fcr_bsp":
            return (
                self.coordinator.get_fcr(
                    "bsp"
                )
            )

        if key == "fcr_stream":
            return (
                self.coordinator.get_fcr(
                    "stream"
                )
            )

        #
        # Cloud data
        #
        if key == "belpex_average":
            return (
                self.coordinator.get_cloud(
                    "belpex_average"
                )
            )
        #
        # AWS QOS
        #
        if key == "aws_qos":
            return (
                self.coordinator.get_metadata(
                    "aws_qos"
                )
            )
        #
        # BMS data
        #
        if key == "bms_status":
            return (
                self.coordinator.get_metadata(
                    "bms_status"
                )
            )
        if key == "bms_model":
            return (
                self.coordinator.get_metadata(
                    "bms_model"
                )
            )
        #
        # Board model
        #
        if key == "board_model":
            return (
                self.coordinator.get_metadata(
                    "board_model"
                )
            )
        if key == "device_name":
            return (
                self.coordinator.get_metadata(
                    "device_name"
                )
            )
        #
        # Connected status
        #
        if key == "connected_status":
            return (
                self.coordinator.get_metadata(
                    "connected_status"
                )
            )
        #
        # Eastron QoS
        #
        if key == "eastron_qos":
            return (
                self.coordinator.get_metadata(
                    "eastron_qos"
                )
            )

        if key == "ev_status":
            return (
                self.coordinator.get_metadata(
                    "ev_status"
                )
            )
        if key == "ev_discovery":
            return (
                self.coordinator.get_metadata(
                    "ev_discovery"
                )
            )
        if key == "inverter_status":
            return (
                self.coordinator.get_metadata(
                    "inverter_status"
                )
            )

        if key == "inverter_meter":
            return (
                self.coordinator.get_metadata(
                    "inverter_meter"
                )
            )

        if key == "inverter_fw":
            return (
                self.coordinator.get_metadata(
                    "inverter_fw"
                )
            )
        if key == "inverter_serial":
            return (
                self.coordinator.get_metadata(
                    "inverter_serial"
                )
            )
        if key == "ioapi":
            return (
                self.coordinator.get_metadata(
                    "ioapi"
                )
            )
        if key == "iodaemon":
            return (
                self.coordinator.get_metadata(
                    "iodaemon"
                )
            )
        if key == "iomanager":
            return (
                self.coordinator.get_metadata(
                    "iomanager"
                )
            )
        if key == "update_status":
            return (
                self.coordinator.get_metadata(
                    "update_status"
                )
            )
        if key == "modbus_details":
            return (
                self.coordinator.get_metadata(
                    "modbus_details"
                )
            )

        if key == "modbus_qos":
            return (
                self.coordinator.get_metadata(
                    "modbus_qos"
                )
            )

        if key == "modbus_adapter":
            return (
                self.coordinator.get_metadata(
                    "modbus_adapter"
                )
            )
        if key == "p1_status":
            return self.coordinator.get_metadata(
                "p1_status"
            )

        if key == "p1_qos":
            return self.coordinator.get_metadata(
                "p1_qos"
            )

        if key == "p1_gridtype":
            return self.coordinator.get_metadata(
                "p1_gridtype"
            )
        if key == "storage_details":
            return (
                self.coordinator.get_metadata(
                    "storage_details"
                )
            )

        return None

    @property
    def extra_state_attributes(
        self,
    ):
        """Additional information."""

        if (
            self._definition["key"]
            == "belpex_average"
        ):
            return {
                "price_points":
                    self.coordinator.get_cloud(
                        "price_points"
                    ),
                "has_future_prices":
                    self.coordinator.get_cloud(
                        "has_future_prices"
                    ),
            }

        return {}

# ============================================================
# EMS SENSORS
# ============================================================
class LifepowrEMSConfSensor(
    CoordinatorEntity,
    SensorEntity,
):
    """EMS configuration sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: LifepowrCoordinator,
        entry: ConfigEntry,
        definition: dict,
    ) -> None:
        super().__init__(coordinator)

        self._definition = definition

        self._attr_name = definition["name"]

        self._attr_unique_id = (
            f"lifepowr_{entry.entry_id}_ems_"
            f"{definition['key']}"
        )

        self._attr_icon = definition.get(
            "icon"
        )

        self._attr_native_unit_of_measurement = (
            definition.get("unit")
        )

    @property
    def native_value(self):
        return self.coordinator.get_emsconf(
            self._definition["key"]
        )

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={
                (
                    DOMAIN,
                    self.coordinator.get_device_identifier(),
                )
            },
            name="LifePowr FlexiO",
            manufacturer=MANUFACTURER,
            model=MODEL,
            configuration_url=f"http://{self.coordinator.host}",
        )