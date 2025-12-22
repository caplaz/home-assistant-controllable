"""The Controllable integration.

This integration allows creating virtual switches that control existing entities
on devices, with sync status tracking to detect when the real device changes
externally.
"""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Event, HomeAssistant, callback

from .const import CONF_TARGET_ENTITY, DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["switch"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Controllable from a config entry.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry for this integration.

    Returns:
        True if setup was successful.
    """
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Listen for state changes on target entities
    @callback
    def async_state_changed(event: Event) -> None:
        """Handle state changes for target entities.

        When a target entity changes state externally, notify the controllable
        switches to update their sync status.

        Args:
            event: The state changed event.
        """
        entity_id = event.data.get("entity_id")
        if entity_id in [
            data[CONF_TARGET_ENTITY]
            for data in hass.data[DOMAIN].values()
            if CONF_TARGET_ENTITY in data
        ]:
            # Notify switches to update sync status
            event_name = f"{DOMAIN}_target_changed"
            event_data = {"entity_id": entity_id}
            hass.bus.async_fire(event_name, event_data)

    hass.bus.async_listen("state_changed", async_state_changed)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry for this integration.

    Returns:
        True if unload was successful.
    """
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
