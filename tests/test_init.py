"""Test Controllable integration."""

from unittest.mock import MagicMock

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from custom_components.controllable import async_setup_entry, async_unload_entry


async def test_setup_and_unload(hass: HomeAssistant):
    """Test setup and unload."""
    config_entry = MagicMock(spec=ConfigEntry)
    config_entry.entry_id = "test_entry"
    config_entry.data = {"name": "Test", "target_entity": "switch.test"}
    assert await async_setup_entry(hass, config_entry)
    assert await async_unload_entry(hass, config_entry)
