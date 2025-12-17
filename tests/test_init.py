"""Test Controllable integration."""

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from custom_components.controllable import async_setup_entry, async_unload_entry
from custom_components.controllable.const import DOMAIN


async def test_setup_and_unload(hass: HomeAssistant, config_entry: ConfigEntry):
    """Test setup and unload."""
    assert await async_setup_entry(hass, config_entry)
    assert await async_unload_entry(hass, config_entry)