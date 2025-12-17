# Controllable

A Home Assistant integration that provides virtual switch entities that proxy real entities, tracking synchronization to prevent automation overrides.

## Installation

### HACS (Recommended)

1. Add this repository to HACS as a custom repository.
2. Install the "Controllable" integration.
3. Restart Home Assistant.

### Manual

1. Copy the `custom_components/controllable` folder to your Home Assistant's `custom_components` directory.
2. Restart Home Assistant.

## Configuration

After installation, add a new "Controllable" integration via the UI:

1. Go to Settings > Devices & Services > Add Integration.
2. Search for "Controllable" and select it.
3. Enter a name and select the target entity (switch, light, or fan).
4. The virtual switch will appear in your entities and be added to the target's device.

## Usage

- The virtual switch mirrors the state of the target entity.
- When states match, `is_synced` is true.
- If the target is changed manually, `is_synced` becomes false, preventing automations from overriding until states match again.
- Turning the virtual switch on/off will control the target and set `is_synced` to true.

## Attributes

- `is_synced`: Boolean indicating if virtual and real states match.
- `target_entity`: The entity ID of the proxied entity.

## Support

For issues or feature requests, please create an issue on GitHub.
