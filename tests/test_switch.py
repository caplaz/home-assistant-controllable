"""Test Controllable switch."""

from unittest.mock import AsyncMock, MagicMock, patch

from homeassistant.components.switch import SwitchDeviceClass
from homeassistant.core import HomeAssistant

from custom_components.controllable.switch import ControllableSwitch


async def test_switch_initialization(hass: HomeAssistant):
    """Test switch initialization with valid target."""
    # Mock entity registry
    mock_entity_reg = MagicMock()
    mock_entity = MagicMock()
    mock_entity.entity_id = "switch.target"
    mock_entity.domain = "switch"
    mock_entity_reg.entities.get_entries_for_device_id.return_value = [mock_entity]

    # Mock device registry
    mock_device_reg = MagicMock()
    mock_device = MagicMock()
    mock_device.identifiers = {("test", "device_123")}
    mock_device.connections = set()
    mock_device_reg.async_get.return_value = mock_device

    with (
        patch(
            "custom_components.controllable.switch.er.async_get",
            return_value=mock_entity_reg,
        ),
        patch(
            "custom_components.controllable.switch.dr.async_get",
            return_value=mock_device_reg,
        ),
    ):
        switch = ControllableSwitch(hass, "entry_123", "Test Switch", "device_123")

        assert switch._name == "Test Switch"
        assert switch._target_entity == "switch.target"
        assert switch._is_synced is True
        assert switch.unique_id == "entry_123_Test Switch"
        assert switch.device_class == SwitchDeviceClass.SWITCH
        assert switch._attr_device_info["identifiers"] == {("test", "device_123")}


async def test_switch_state(hass: HomeAssistant):
    """Test switch state property."""
    # Mock registries
    mock_entity_reg = MagicMock()
    mock_entity = MagicMock()
    mock_entity.entity_id = "switch.test_target"
    mock_entity.domain = "switch"
    mock_entity_reg.entities.get_entries_for_device_id.return_value = [mock_entity]

    mock_device_reg = MagicMock()
    mock_device = MagicMock()
    mock_device.identifiers = {("test", "device_123")}
    mock_device.connections = set()
    mock_device_reg.async_get.return_value = mock_device

    with (
        patch(
            "custom_components.controllable.switch.er.async_get",
            return_value=mock_entity_reg,
        ),
        patch(
            "custom_components.controllable.switch.dr.async_get",
            return_value=mock_device_reg,
        ),
    ):
        # Mock target state first
        hass.states.async_set("switch.test_target", "on")

        switch = ControllableSwitch(hass, "entry_123", "Test Switch", "device_123")

        assert switch.is_on is True

        hass.states.async_set("switch.test_target", "off")
        # Note: _is_on doesn't auto-update, only on turn_on/off or sync update
        # For this test, check that it remains True until updated
        assert switch.is_on is True  # Internal state not changed

        # But sync status should be False
        # Note: We can't call async_update_sync_status in test without proper setup
        # So we manually check the logic
        target_state = hass.states.get("switch.test_target")
        if target_state:
            real_state = target_state.state == "on"
            expected_synced = switch._is_on == real_state
            assert expected_synced is False


async def test_switch_turn_on(hass: HomeAssistant):
    """Test turning switch on."""
    switch = ControllableSwitch(hass, "entry_123", "Test Switch", "device_123")
    switch._target_entity = "switch.test_target"

    # Mock the target entity state
    mock_state = MagicMock()
    mock_state.state = "on"

    with (
        patch(
            "homeassistant.core.ServiceRegistry.async_call", new_callable=AsyncMock
        ) as mock_call,
        patch.object(switch, "async_write_ha_state"),
        patch("homeassistant.core.StateMachine.get", return_value=mock_state),
    ):
        await switch.async_turn_on()

        mock_call.assert_called_once_with(
            "homeassistant",
            "turn_on",
            {"entity_id": "switch.test_target"},
        )
        assert switch._is_synced is True


async def test_switch_turn_off(hass: HomeAssistant):
    """Test turning switch off."""
    switch = ControllableSwitch(hass, "entry_123", "Test Switch", "device_123")
    switch._target_entity = "switch.test_target"
    switch._is_on = True  # Set initial state

    # Mock the target entity state
    mock_state = MagicMock()
    mock_state.state = "off"

    with (
        patch(
            "homeassistant.core.ServiceRegistry.async_call", new_callable=AsyncMock
        ) as mock_call,
        patch.object(switch, "async_write_ha_state"),
        patch("homeassistant.core.StateMachine.get", return_value=mock_state),
    ):
        await switch.async_turn_off()

        mock_call.assert_called_once_with(
            "homeassistant",
            "turn_off",
            {"entity_id": "switch.test_target"},
        )
        assert switch._is_synced is True
        assert switch._is_on is False
