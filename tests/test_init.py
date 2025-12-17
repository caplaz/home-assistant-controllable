"""Test Controllable integration setup and unload."""

from unittest.mock import MagicMock, patch

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from custom_components.controllable import async_setup_entry, async_unload_entry


async def test_setup_and_unload(hass: HomeAssistant):
    """Test setup and unload of the integration."""
    config_entry = MagicMock(spec=ConfigEntry)
    config_entry.entry_id = "test_entry"
    config_entry.domain = "controllable"
    config_entry.title = "Test Controllable"
    config_entry.data = {
        "name": "Test",
        "target_entity": "switch.test",
    }

    # Mock the forward_entry_setups to avoid actual setup
    with patch.object(
        hass.config_entries, "async_forward_entry_setups", return_value=None
    ):
        result = await async_setup_entry(hass, config_entry)
        assert result is True

    # Mock the unload_platforms
    with patch.object(hass.config_entries, "async_unload_platforms", return_value=True):
        result = await async_unload_entry(hass, config_entry)
        assert result is True


async def test_setup_with_invalid_data(hass: HomeAssistant):
    """Test setup with invalid config data."""
    config_entry = MagicMock(spec=ConfigEntry)
    config_entry.entry_id = "test_entry"
    config_entry.domain = "controllable"
    config_entry.title = "Test Controllable"
    config_entry.data = {
        "name": "Test",
        # Missing target_entity
    }

    # Mock the forward_entry_setups
    with patch.object(
        hass.config_entries, "async_forward_entry_setups", return_value=None
    ):
        result = await async_setup_entry(hass, config_entry)
        assert result is True


async def test_unload_without_setup(hass: HomeAssistant):
    """Test unload when not set up."""
    config_entry = MagicMock(spec=ConfigEntry)
    config_entry.entry_id = "test_entry"
    config_entry.domain = "controllable"
    config_entry.title = "Test Controllable"

    # Mock the unload_platforms to return False
    with patch.object(
        hass.config_entries, "async_unload_platforms", return_value=False
    ):
        result = await async_unload_entry(hass, config_entry)
        assert result is False


async def test_state_change_listener(hass: HomeAssistant):
    """Test that state change events are listened to."""
    config_entry = MagicMock(spec=ConfigEntry)
    config_entry.entry_id = "test_entry"
    config_entry.domain = "controllable"
    config_entry.title = "Test Controllable"
    config_entry.data = {
        "name": "Test",
        "target_entity": "switch.test",
    }

    with patch.object(
        hass.config_entries, "async_forward_entry_setups", return_value=None
    ):
        await async_setup_entry(hass, config_entry)

        # Check that the listener was added (basic check)
        assert config_entry.entry_id in hass.data.get("controllable", {})

        with patch.object(
            hass.config_entries, "async_unload_platforms", return_value=True
        ):
            await async_unload_entry(hass, config_entry)
