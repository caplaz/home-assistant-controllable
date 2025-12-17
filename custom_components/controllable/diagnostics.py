"""Diagnostics for Controllable integration."""

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    data = config_entry.data
    diagnostics = {
        "config_entry": {
            "entry_id": config_entry.entry_id,
            "data": data,
        },
        "entities": [],
    }

    # Get entities for this config entry
    for state in hass.states.async_all():
        entity_id = state.entity_id
        if entity_id.startswith(f"{DOMAIN}."):
            diagnostics["entities"].append(  # type: ignore [attr-defined]
                {
                    "entity_id": entity_id,
                    "state": state.state,
                    "attributes": dict(state.attributes),
                }
            )

    return diagnostics
