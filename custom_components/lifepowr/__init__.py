"""The LifePowr FlexiO integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_HOST, DOMAIN
from .coordinator import LifepowrCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
]


async def async_setup(
    hass: HomeAssistant,
    config: dict,
) -> bool:
    """Set up via YAML."""

    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up LifePowr from a config entry."""

    host = entry.data[CONF_HOST]

    coordinator = LifepowrCoordinator(
        hass=hass,
        host=host,
    )

    coordinator.start()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    entry.async_on_unload(
        entry.add_update_listener(
            async_reload_entry
        )
    )
    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload a config entry."""

    unload_ok = (
        await hass.config_entries.async_unload_platforms(
            entry,
            PLATFORMS,
        )
    )

    if not unload_ok:
        return False

    coordinator: LifepowrCoordinator = (
        hass.data[DOMAIN][entry.entry_id]
    )

    await coordinator.stop()

    hass.data[DOMAIN].pop(
        entry.entry_id,
        None,
    )

    if not hass.data[DOMAIN]:
        hass.data.pop(
            DOMAIN,
            None,
        )
    return True


async def async_reload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> None:
    """Reload config entry."""

    await async_unload_entry(
        hass,
        entry,
    )

    await async_setup_entry(
        hass,
        entry,
    )