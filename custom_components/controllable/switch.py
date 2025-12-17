"""Switch platform for Controllable integration.

Provides the ControllableSwitch entity that creates virtual switches
associated with devices, controlling their main controllable entities.
"""

import logging
from typing import Any

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    ATTR_IS_SYNCED,
    ATTR_TARGET_ENTITY,
    CONF_NAME,
    CONF_TARGET_DEVICE,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Controllable switch.

    Creates a ControllableSwitch entity for the config entry.

    Args:
        hass: The Home Assistant instance.
        config_entry: The config entry for this controllable.
        async_add_entities: Callback to add entities.
    """
    data = config_entry.data
    name = data[CONF_NAME]
    target_device = data[CONF_TARGET_DEVICE]

    entity = ControllableSwitch(hass, config_entry.entry_id, name, target_device)
    async_add_entities([entity])

    # Listen for target changes
    if entity._target_entity:

        @callback
        def async_target_changed(event):
            """Update sync status when target changes.

            Args:
                event: The custom event with entity_id.
            """
            if event.data.get("entity_id") == entity._target_entity:
                entity.async_update_sync_status()

        hass.bus.async_listen(f"{DOMAIN}_target_changed", async_target_changed)


class ControllableSwitch(SwitchEntity):
    """Representation of a Controllable switch.

    A virtual switch that controls a target entity on a device,
    with sync status tracking.
    """

    def __init__(
        self, hass: HomeAssistant, entry_id: str, name: str, target_device: str
    ) -> None:
        """Initialize the switch.

        Args:
            hass: The Home Assistant instance.
            entry_id: The config entry ID.
            name: The name of the controllable switch.
            target_device: The device ID to control.
        """
        self.hass = hass
        self._entry_id = entry_id
        self._name = name
        self._target_device = target_device
        self._is_synced = True  # Assume synced initially
        self._is_on: bool | None = None  # Internal state, separate from target
        self._attr_unique_id = f"{entry_id}_{name}"
        self._attr_name = name
        self._attr_device_class = SwitchDeviceClass.SWITCH

        # Find target entity on the device
        entity_reg = er.async_get(hass)
        entities = entity_reg.entities.get_entries_for_device_id(target_device)
        controllable_domains = {"switch", "light", "fan"}
        target_entity_entry = next(
            (e for e in entities if e.domain in controllable_domains), None
        )
        self._target_entity: str | None = None
        if target_entity_entry:
            self._target_entity = target_entity_entry.entity_id
            _LOGGER.info(
                "Controllable %s will control %s",
                self._name,
                self._target_entity,
            )
        else:
            self._target_entity = None
            _LOGGER.error("No controllable entity found on device %s", target_device)

        # Get device info to properly associate with existing device
        device_reg = dr.async_get(hass)
        device = device_reg.async_get(target_device)
        if device:
            # Use the device's identifiers to link this entity to the same device
            self._attr_device_info = {
                "identifiers": device.identifiers,
                "connections": device.connections,
            }
            _LOGGER.info(
                "Controllable %s associated with device %s using identifiers %s",
                self._name,
                target_device,
                device.identifiers,
            )
        else:
            _LOGGER.error("Device %s not found", target_device)

        # Initialize internal state to match target
        if self._target_entity:
            target_state = self.hass.states.get(self._target_entity)
            if target_state:
                self._is_on = target_state.state == "on"
            else:
                self._is_on = False

    @property
    def is_on(self) -> bool | None:
        """Return true if the switch is on."""
        return self._is_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on.

        Turns on the target entity and updates sync status.

        Args:
            **kwargs: Additional arguments (unused).
        """
        self._is_on = True
        await self.hass.services.async_call(
            "homeassistant", "turn_on", {"entity_id": self._target_entity}
        )
        self.async_update_sync_status()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off.

        Turns off the target entity and updates sync status.

        Args:
            **kwargs: Additional arguments (unused).
        """
        self._is_on = False
        await self.hass.services.async_call(
            "homeassistant", "turn_off", {"entity_id": self._target_entity}
        )
        self.async_update_sync_status()
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes.

        Returns:
            Dictionary with sync status and target entity.
        """
        return {
            ATTR_IS_SYNCED: self._is_synced,
            ATTR_TARGET_ENTITY: self._target_entity,
        }

    @callback
    def async_update_sync_status(self) -> None:
        """Update the sync status based on current states.

        Checks if the internal state matches the target entity's state.
        """
        if self._target_entity:
            target_state = self.hass.states.get(self._target_entity)
            if target_state:
                real_state = target_state.state == "on"
                self._is_synced = self._is_on == real_state
            else:
                self._is_synced = False
        else:
            self._is_synced = False
        self.async_write_ha_state()
