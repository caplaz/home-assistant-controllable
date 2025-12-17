"""Config flow for Controllable integration."""

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import DOMAIN, CONF_NAME, CONF_TARGET_ENTITY

_LOGGER = logging.getLogger(__name__)


class ControllableConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Controllable."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate target entity
            target_entity = user_input[CONF_TARGET_ENTITY]
            if not self._is_valid_target(self.hass, target_entity):
                errors[CONF_TARGET_ENTITY] = "invalid_target"
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
                    vol.Required(CONF_TARGET_ENTITY): selector.EntitySelector(
                        selector.EntitySelectorConfig(domain=["switch", "light", "fan"])
                    ),
                }
            ),
            errors=errors,
        )

    def _is_valid_target(self, hass: HomeAssistant, entity_id: str) -> bool:
        """Check if the target entity supports turn_on/turn_off."""
        state = hass.states.get(entity_id)
        if not state:
            return False
        domain = entity_id.split(".")[0]
        return domain in ["switch", "light", "fan"]