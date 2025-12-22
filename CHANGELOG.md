# Changelog

## 1.0.1 - 2025-12-22

### Fixed

- KeyError: 'target_entity' when handling state changes for config entries missing the target_entity key

## 1.0.0 - 2025-12-17

### Added

- Initial release of Controllable integration
- Virtual switch entities that proxy real Home Assistant entities
- Synchronization tracking to prevent automation overrides
- UI configuration flow with entity selector
- Support for switch, light, and fan entities
- Entities added to target's device registry
- Event-driven sync updates
- Diagnostics and logging support
- Bronze quality scale compliance

### Features

- `is_synced` attribute indicates state synchronization
- `target_entity` attribute shows proxied entity
- Automatic sync restoration when states match
