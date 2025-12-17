"""Test Controllable switch."""

from unittest.mock import AsyncMock, MagicMock, patch

from homeassistant.components.switch import SwitchDeviceClass
from homeassistant.core import HomeAssistant

from custom_components.controllable.switch import ControllableSwitch


async def test_switch_initialization(hass: HomeAssistant):
    """Test switch initialization."""
    # Mock entity registry
    mock_entity_reg = MagicMock()
    mock_entity = MagicMock()
    mock_entity.device_id = "device_123"
    mock_entity_reg.async_get.return_value = mock_entity

    with patch(
        "custom_components.controllable.switch.er.async_get",
        return_value=mock_entity_reg,
    ):
        switch = ControllableSwitch(
            hass, "entry_123", "Test Switch", "switch.test_target"
        )

        assert switch._name == "Test Switch"
        assert switch._target_entity == "switch.test_target"
        assert switch._is_synced is True
        assert switch.unique_id == "entry_123_Test Switch"
        assert switch.device_class == SwitchDeviceClass.SWITCH
        assert switch._attr_device_id == "device_123"


async def test_switch_state(hass: HomeAssistant):
    """Test switch state property."""
    # Mock target state first
    hass.states.async_set("switch.test_target", "on")

    switch = ControllableSwitch(hass, "entry_123", "Test Switch", "switch.test_target")

    assert switch.is_on is True

    hass.states.async_set("switch.test_target", "off")
    # Note: _is_on doesn't auto-update, only on turn_on/off or sync update
    # For this test, check that it remains True until updated
    assert switch.is_on is True  # Internal state not changed

    # But sync status should be False
    switch.async_update_sync_status()
    assert switch._is_synced is False


async def test_switch_turn_on(hass: HomeAssistant):
    """Test turning switch on."""
    switch = ControllableSwitch(hass, "entry_123", "Test Switch", "switch.test_target")

    with patch.object(hass.services, "async_call", new_callable=AsyncMock) as mock_call:
        await switch.async_turn_on()

        mock_call.assert_called_once_with(
            "homeassistant", "turn_on", {"entity_id": "switch.test_target"}
        )
        assert switch._is_synced is True


async def test_switch_attributes(hass: HomeAssistant):
    """Test switch attributes."""
    switch = ControllableSwitch(hass, "entry_123", "Test Switch", "switch.test_target")
    switch._is_synced = False

    attrs = switch.extra_state_attributes

    assert attrs["is_synced"] is False
    assert attrs["target_entity"] == "switch.test_target"
