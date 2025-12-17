"""Options flow for Controllable integration."""

import logging
from typing import Any

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector
import voluptuous as vol

from .const import CONF_NAME, CONF_TARGET_ENTITY

_LOGGER = logging.getLogger(__name__)


class ControllableOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Controllable."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate target entity
            target_entity = user_input[CONF_TARGET_ENTITY]
            if not self._is_valid_target(self.hass, target_entity):
                errors[CONF_TARGET_ENTITY] = "invalid_target"
            else:
                return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_NAME, default=self.config_entry.data.get(CONF_NAME)
                    ): str,
                    vol.Required(
                        CONF_TARGET_ENTITY,
                        default=self.config_entry.data.get(CONF_TARGET_ENTITY),
                    ): selector.EntitySelector(
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
