# Controllable

[![hacs][hacsbadge]][hacs]
[![GitHub Release][releases-shield]][releases]
[![CI][ci-shield]][ci]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

A Home Assistant custom integration that provides virtual switch entities that proxy real entities, tracking synchronization to prevent automation overrides.

## How It Works

### Overview

The Controllable integration creates virtual switch entities that intelligently proxy real Home Assistant entities (switches, lights, fans). It maintains synchronization between virtual and real states, preventing automations from overriding manual changes until states realign.

```
Real Entity → Virtual Switch → Automation Control
     ↑              ↓              ↓
  Manual Change  Sync Check    Prevent Override
     ↓              ↓              ↓
State Mismatch → is_synced=false → Block Automation
```

### Key Features

- **Virtual Proxying**: Virtual switches control real entities while tracking state sync
- **Sync Tracking**: `is_synced` attribute shows synchronization status
- **Automation Protection**: Prevents automations from overriding manual changes
- **Device Integration**: Virtual switches appear in the target's device registry
- **Event-Driven Updates**: Real-time sync monitoring via Home Assistant events

### Synchronization Logic

1. **Initial State**: Virtual switch mirrors real entity state, `is_synced=true`
2. **Virtual Control**: Turning virtual switch controls real entity, maintains `is_synced=true`
3. **Manual Override**: Manual changes to real entity break sync, `is_synced=false`
4. **Sync Restoration**: When states match again, `is_synced` becomes true

## Installation

### Method 1: HACS (Recommended)

HACS is the easiest way to install custom integrations.

#### Prerequisites

- [HACS](https://hacs.xyz/) installed in Home Assistant
- Home Assistant version 2024.1.0 or higher

#### Installation Steps

1. **Open HACS**: Go to HACS in your Home Assistant sidebar
2. **Navigate to Integrations**: Click on "Integrations"
3. **Search and Install**:
   - Search for "Controllable" in HACS
   - Click on it and select "Download"
   - Choose the latest version
4. **Restart Home Assistant**: Required for the integration to load

### Method 2: Manual Installation

#### Prerequisites

- Home Assistant version 2024.1.0 or higher

#### Installation Steps

1. **Download the Integration**:

   ```bash
   wget https://github.com/yourusername/controllable/archive/refs/tags/v1.0.0.zip
   unzip v1.0.0.zip
   ```

2. **Copy Files**:

   ```bash
   cp -r controllable-1.0.0/custom_components/controllable /config/custom_components/
   ```

3. **Restart Home Assistant**:
   - Go to Settings → System → Restart
   - Wait for Home Assistant to restart

## Configuration

### Initial Setup

1. **Add Integration**: Go to Settings → Devices & Services → Add Integration
2. **Search**: Type "Controllable" in the search box
3. **Select**: Click on "Controllable" from the results
4. **Configure**:
   - **Name**: Friendly name for the virtual switch
   - **Target Entity**: Select the real entity to proxy (switch, light, or fan)
5. **Submit**: The integration creates the virtual switch

### Usage

The integration creates virtual switch entities that:

- **Control Real Entities**: Turning on/off controls the target entity
- **Track Synchronization**: `is_synced` shows if states match
- **Prevent Automation Conflicts**: Automations respect manual overrides
- **Device Grouping**: Virtual switches appear in target's device

### Entity Attributes

- `is_synced`: Boolean indicating synchronization status
- `target_entity`: Entity ID of the proxied real entity

### Dashboard Integration

Add virtual switches to your dashboard like any other switch:

1. **Add Card**: Dashboard → Add Card → Entities
2. **Select Entities**: Choose controllable switches
3. **Customize**: Set display options and icons

## Troubleshooting

### Common Issues

#### Sync Not Working

- **Cause**: Target entity changed externally
- **Solution**: Manually sync by turning virtual switch to match real state

#### Entity Unavailable

- **Cause**: Target entity removed or unavailable
- **Solution**: Reconfigure the controllable with a valid target

#### Automation Still Triggers

- **Cause**: Automation not checking `is_synced`
- **Solution**: Add condition to check `is_synced` attribute

### Debug Logging

Enable debug logging:

```yaml
logger:
  logs:
    custom_components.controllable: debug
```

### Testing

Use the development script:

```bash
./dev.sh start    # Start HA dev environment
./dev.sh test     # Run tests
./dev.sh logs     # Check logs
```

## Technical Details

### Architecture

- **Event-Driven**: Uses Home Assistant events for real-time sync
- **No Polling**: Efficient listener-based updates
- **Device Registry**: Virtual entities grouped with targets
- **Config Flow**: User-friendly setup and reconfiguration
- **Error Handling**: Graceful failure recovery

### Requirements

- **Home Assistant**: 2024.1.0+
- **Python Packages**: `voluptuous>=0.13.1`

### Supported Entities

- Switches
- Lights
- Fans

### API Usage

- Internal Home Assistant APIs only
- No external dependencies
- Local state management

## Contributing

### Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/controllable.git
   cd controllable
   ```

2. Install development dependencies:

   ```bash
   pip install -r requirements-dev.txt
   ```

3. Run tests:
   ```bash
   python -m pytest
   ```

### Code Quality

- **Linting**: black, isort, flake8, mypy
- **Testing**: pytest with coverage
- **CI**: Automated checks on PRs

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<!-- Badges -->

[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/yourusername/controllable.svg?style=for-the-badge
[releases]: https://github.com/yourusername/controllable/releases
[ci-shield]: https://img.shields.io/github/actions/workflow/status/yourusername/controllable/ci.yml?style=for-the-badge
[ci]: https://github.com/yourusername/controllable/actions/workflows/ci.yml
[commits-shield]: https://img.shields.io/github/commit-activity/m/yourusername/controllable?style=for-the-badge
[commits]: https://github.com/yourusername/controllable/commits/main
[license-shield]: https://img.shields.io/github/license/yourusername/controllable.svg?style=for-the-badge
