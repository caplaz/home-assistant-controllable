"""Config flow for Controllable integration.

Handles the setup flow for creating controllable switches that control
entities on selected devices.
"""

import logging
from typing import Any

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import device_registry as dr, entity_registry as er, selector
import voluptuous as vol

from .const import CONF_NAME, CONF_TARGET_DEVICE, DOMAIN

_LOGGER = logging.getLogger(__name__)


class ControllableConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Controllable.

    This flow allows users to select a device and create a controllable
    switch that controls the main controllable entity on that device.
    """

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step.

        Prompts the user to enter a name and select a target device.

        Args:
            user_input: The user input from the form.

        Returns:
            The next flow step result.
        """
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate target device
            target_device = user_input[CONF_TARGET_DEVICE]
            if not self._is_valid_device(self.hass, target_device):
                errors[CONF_TARGET_DEVICE] = "invalid_device"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME): str,
                    vol.Required(CONF_TARGET_DEVICE): selector.DeviceSelector(),
                }
            ),
            errors=errors,
        )

    def _is_valid_device(self, hass: HomeAssistant, device_id: str) -> bool:
        """Check if the device exists and has controllable entities.

        A device is valid if it exists and has at least one entity
        in the switch, light, or fan domains.

        Args:
            hass: The Home Assistant instance.
            device_id: The device ID to validate.

        Returns:
            True if the device is valid.
        """
        device_reg = dr.async_get(hass)
        device = device_reg.async_get(device_id)
        if not device:
            return False

        entity_reg = er.async_get(hass)
        entities = entity_reg.entities.get_entries_for_device_id(device_id)
        controllable_domains = {"switch", "light", "fan"}
        return any(entity.domain in controllable_domains for entity in entities)
