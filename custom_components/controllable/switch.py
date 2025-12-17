"""Switch platform for Controllable integration."""

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    ATTR_IS_SYNCED,
    ATTR_TARGET_ENTITY,
    CONF_NAME,
    CONF_TARGET_ENTITY,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Controllable switch."""
    data = config_entry.data
    name = data[CONF_NAME]
    target_entity = data[CONF_TARGET_ENTITY]

    entity = ControllableSwitch(hass, config_entry.entry_id, name, target_entity)
    async_add_entities([entity])

    # Listen for target changes
    @callback
    def async_target_changed(event):
        """Update sync status when target changes."""
        if event.data.get("entity_id") == target_entity:
            entity.async_update_sync_status()

    hass.bus.async_listen(f"{DOMAIN}_target_changed", async_target_changed)


class ControllableSwitch(SwitchEntity):
    """Representation of a Controllable switch."""

    def __init__(
        self, hass: HomeAssistant, entry_id: str, name: str, target_entity: str
    ) -> None:
        """Initialize the switch."""
        self.hass = hass
        self._entry_id = entry_id
        self._name = name
        self._target_entity = target_entity
        self._is_synced = True  # Assume synced initially
        self._is_on = None  # Internal state, separate from target
        self._attr_unique_id = f"{entry_id}_{name}"
        self._attr_name = name
        self._attr_device_class = "switch"

        # Set device_id to target's device
        entity_reg = er.async_get(hass)
        target_entry = entity_reg.async_get(target_entity)
        if target_entry and target_entry.device_id:
            self._attr_device_id = target_entry.device_id

        # Initialize internal state to match target
        target_state = self.hass.states.get(target_entity)
        if target_state:
            self._is_on = target_state.state == "on"
        else:
            self._is_on = False

    @property
    def is_on(self) -> bool | None:
        """Return true if the switch is on."""
        return self._is_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        self._is_on = True
        await self.hass.services.async_call(
            "homeassistant", "turn_on", {"entity_id": self._target_entity}
        )
        self.async_update_sync_status()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        self._is_on = False
        await self.hass.services.async_call(
            "homeassistant", "turn_off", {"entity_id": self._target_entity}
        )
        self.async_update_sync_status()
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            ATTR_IS_SYNCED: self._is_synced,
            ATTR_TARGET_ENTITY: self._target_entity,
        }

    @callback
    def async_update_sync_status(self) -> None:
        """Update the sync status based on current states."""
        target_state = self.hass.states.get(self._target_entity)
        if target_state:
            real_state = target_state.state == "on"
            self._is_synced = self._is_on == real_state
        else:
            self._is_synced = False
        self.async_write_ha_state()
