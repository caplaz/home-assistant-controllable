# Controllable

[![hacs][hacsbadge]][hacs]
[![GitHub Release][releases-shield]][releases]
[![CI][ci-shield]][ci]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

A Home Assistant custom integration that provides virtual switch entities that proxy real entities, tracking synchronization to prevent automation overrides.

## What Does This Do?

The **Controllable** integration solves a common Home Assistant problem: **automation conflicts with manual control**.

### The Problem

```
Scenario: You have a smart light controlled by both automation AND manual control

1. Automation turns light ON
2. You manually turn it OFF
3. Automation immediately turns it back ON (because the automation still thinks it should be on)
4. Frustration! 😤
```

### The Solution

Controllable creates an **intermediary virtual switch** that tracks whether manual changes have been made:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        HOME ASSISTANT                               │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                   YOUR AUTOMATIONS                           │ │
│  │         (Bedroom Light Turn On @ Sunrise)                   │ │
│  └────────────────────────┬─────────────────────────────────────┘ │
│                           │                                        │
│                           ▼                                        │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │         CONTROLLABLE VIRTUAL SWITCH (Proxy)                 │ │
│  │                                                              │ │
│  │  • Passes commands to real light                            │ │
│  │  • Tracks sync status (is_synced)                           │ │
│  │  • Blocks automation if manually overridden                 │ │
│  └────────────────────────┬─────────────────────────────────────┘ │
│                           │                                        │
│                    ┌──────┴──────┐                                 │
│                    ▼             ▼                                 │
│  ┌───────────────────────┐  ┌──────────────────┐                 │
│  │  REAL LIGHT ENTITY    │  │  MANUAL CONTROL  │                 │
│  │   (switch.bedroom)    │  │   (Wall Switch)  │                 │
│  └───────────────────────┘  └──────────────────┘                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### How It Works

| Step                     | What Happens                                              | is_synced  |
| ------------------------ | --------------------------------------------------------- | ---------- |
| 1️⃣ **Initial State**     | Virtual switch mirrors real entity state                  | `true`     |
| 2️⃣ **Automation Runs**   | Virtual switch controls real entity normally              | `true`     |
| 3️⃣ **Manual Override**   | User changes real entity manually (wall switch, app, etc) | `false` ⚠️ |
| 4️⃣ **Automation Blocks** | Automations check `is_synced` attribute and pause         | `false`    |
| 5️⃣ **Sync Restored**     | When states match again, sync restores                    | `true`     |

## Key Features

✅ **Virtual Proxy Control** - Switches control real entities while tracking sync status
✅ **Sync Tracking** - `is_synced` attribute shows if manual override occurred
✅ **Automation Protection** - Prevents automations from overriding manual changes
✅ **Device Integration** - Virtual switch grouped with target device
✅ **Event-Driven** - Real-time sync monitoring with zero polling
✅ **Simple Setup** - User-friendly config flow in Home Assistant UI

## Who Is This For?

- 🏠 Users with **smart lights/fans on physical switches** (hybrid control)
- 🤖 Anyone using **automations + manual control** on the same device
- 🎯 Users wanting **automation logic respect** for manual overrides
- 📱 Homes with **mobile app, wall switch, and automation** all controlling same device

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
   - **Target Device**: Select a device with a controllable entity (switch, light, or fan)
5. **Submit**: The integration creates the virtual switch

### Supported Entity Types

The integration works with:

- ✅ **Switches** - Light switches, relay switches, etc.
- ✅ **Lights** - Smart bulbs, light strips
- ✅ **Fans** - Ceiling fans, ventilation fans

> **Note**: The target device must have at least one entity in these domains (switch/light/fan) that supports on/off control.

### Usage

The integration creates virtual switch entities that:

- **Control Real Entities**: Turning on/off controls the target entity
- **Track Synchronization**: `is_synced` shows if states match
- **Prevent Automation Conflicts**: Automations can check `is_synced` before running
- **Device Grouping**: Virtual switches appear in target's device

### Entity Attributes

```
switch.bedroom_controllable:
  is_synced: true/false          # Sync status
  target_entity: switch.bedroom  # Real entity being controlled
```

### Using in Automations

Example: Pause automation if user manually changed the light

```yaml
automation:
  - alias: "Bedroom Light at Sunset"
    triggers:
      - platform: sun
        event: sunset
    conditions:
      - condition: state
        entity_id: switch.bedroom_controllable
        attribute: is_synced
        state: "true" # Only run if not manually overridden
    actions:
      - action: light.turn_on
        target:
          entity_id: light.bedroom
```

### Dashboard Integration

Add virtual switches to your dashboard like any other switch:

1. **Add Card**: Dashboard → Add Card → Entities
2. **Select Entities**: Choose controllable switches
3. **Customize**: Set display options and icons
4. **Show Status**: Display `is_synced` attribute for visibility

## Troubleshooting

### Common Issues

#### Sync Not Working

- **Cause**: Target entity changed externally
- **Solution**: Manually sync by turning virtual switch to match real state, or restart HA

#### Entity Unavailable

- **Cause**: Target entity removed or unavailable
- **Solution**: Reconfigure the controllable with a valid target device

#### Automation Still Triggers

- **Cause**: Automation not checking `is_synced`
- **Solution**: Add condition to check `is_synced` attribute in automation

#### Configuration Error: No Controllable Entity Found

- **Cause**: Selected device has no switch/light/fan entities
- **Solution**: Select a different device, or add a controllable entity to the device

### Debug Logging

Enable debug logging to troubleshoot:

```yaml
logger:
  logs:
    custom_components.controllable: debug
```

Then check Settings → System → Logs for "controllable" messages.

### Testing

Use the development script:

```bash
./dev.sh start    # Start HA dev environment
./dev.sh test     # Run pytest
./dev.sh logs     # Check logs
```

## Technical Details

### Architecture

- **Event-Driven**: Uses Home Assistant events for real-time sync updates
- **No Polling**: Efficient listener-based state monitoring
- **Device Registry**: Virtual entities grouped with target devices
- **Config Flow**: Type-safe user-friendly setup
- **Error Handling**: Graceful recovery from entity unavailability

### Device & Entity Filtering

The integration intelligently filters devices and entities:

**Device Selection:**

- Only shows devices that have at least one controllable entity (switch, light, or fan)
- Automatically validates device exists before creation

**Entity Selection:**

- Automatically selects the first switch/light/fan entity on the chosen device
- Falls back gracefully if entity becomes unavailable
- Supports one virtual switch per device

### Requirements

- **Home Assistant**: 2024.1.0+
- **Python Packages**: `voluptuous>=0.13.1`

### Supported Entities

- **Switches**: Standard switch domain entities
- **Lights**: Light domain entities with on/off support
- **Fans**: Fan domain entities with on/off support

### API Usage

- Internal Home Assistant APIs only
- No external API calls
- No external dependencies beyond voluptuous
- All state management is local

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

- **Formatting**: black, isort
- **Linting**: flake8
- **Type Checking**: mypy
- **Security**: bandit
- **Testing**: pytest with comprehensive coverage

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
