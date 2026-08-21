"""Binary sensors for LifePowr FlexiO."""

from __future__ import annotations

import logging
_LOGGER = logging.getLogger(__name__)

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    BINARY_SENSORS,
    DEVICE_FLEXIO_STATUS,
    DOMAIN,
    MANUFACTURER,
    MODEL,
)
from .coordinator import (
    LifepowrCoordinator,
    parse_bool,
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up LifePowr binary sensors."""

    coordinator: LifepowrCoordinator = (
        hass.data[DOMAIN][entry.entry_id]
    )

    entities: list[BinarySensorEntity] = []

    for definition in BINARY_SENSORS:
        entities.append(
            LifepowrDiagnosticBinarySensor(
                coordinator,
                entry,
                definition,
            )
        )

    async_add_entities(entities)


class LifepowrDiagnosticBinarySensor(
    CoordinatorEntity,
    BinarySensorEntity,
):
    """LifePowr diagnostic sensor."""

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

        self._attr_name = definition["name"]

        self._attr_unique_id = (
            f"lifepowr_"
            f"{entry.entry_id}_"
            f"{definition['key']}"
        )
        self._attr_icon = definition.get(
            "icon"
        )

    @property
    def device_info(self):
        """Device information."""
        return self.coordinator.get_device_info()

    @property
    def is_on(self) -> bool:
        """Return binary sensor state."""

        key = self._definition["key"]

        #
        # AWS broker special case
        #
        if key == "aws_broker_ready":
            value = (
                self.coordinator.get_cloud(
                    "aws_broker_ready"
                )
            )
            return parse_bool(value)
        diagnostic = (
            self.coordinator.get_diagnostic(
                key
            )
        )

        if not diagnostic:
            return False

        return parse_bool(
            diagnostic.get(
                "status",
                False,
            )
        )
    @property
    def available(self) -> bool:
        """Entity availability."""

        return self.coordinator.is_available()

    @property
    def extra_state_attributes(
        self,
    ) -> dict:
        """Return attributes."""

        key = self._definition["key"]

        if key == "aws_broker_ready":
            return {
                "source": "/flags/awsBrokerReady",
            }

        diagnostic = (
            self.coordinator.get_diagnostic(
                key
            )
        )

        if not diagnostic:
            return {}

        return {
            "details": diagnostic.get(
                "details"
            ),
            "status": diagnostic.get(
                "status"
            ),
        }
