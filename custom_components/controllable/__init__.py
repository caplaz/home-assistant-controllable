"""The Controllable integration."""

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, Event, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry

from .const import DOMAIN, CONF_TARGET_ENTITY

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["switch"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Controllable from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Listen for state changes on target entities
    @callback
    def async_state_changed(event: Event) -> None:
        """Handle state changes for target entities."""
        entity_id = event.data.get("entity_id")
        if entity_id in [data[CONF_TARGET_ENTITY] for data in hass.data[DOMAIN].values()]:
            # Notify switches to update sync status
            hass.bus.async_fire(f"{DOMAIN}_target_changed", {"entity_id": entity_id})

    hass.bus.async_listen("state_changed", async_state_changed)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok