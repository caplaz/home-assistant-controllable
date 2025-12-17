# Developer Guide

## Development Setup

### Prerequisites

- Python 3.12 or higher
- Home Assistant development environment (optional)
- Git

### Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

### Code Quality Tools

#### Format Code

```bash
black custom_components/
isort custom_components/
```

#### Lint Code

```bash
flake8 custom_components/
mypy custom_components/
bandit -r custom_components/
```

#### Run Tests

```bash
pytest tests/ -v
pytest tests/ -v --cov=custom_components/controllable
```

## Project Structure

```
custom_components/controllable/
├── __init__.py              # Integration setup
├── config_flow.py           # UI configuration flow
├── const.py                 # Constants and configuration
├── manifest.json            # Integration manifest
├── switch.py                # Virtual switch entities
├── strings.json             # UI strings
├── translations/            # UI translations
│   ├── en.json             # English translations
├── diagnostics.py           # Diagnostics support
└── options_flow.py          # Options flow
```

## Development Workflow

### 1. Set up Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/controllable.git
cd controllable

# Set up Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt
```

### 2. Code Changes

- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Write comprehensive docstrings
- Add unit tests for new functionality

### 3. Testing

#### Run All Tests

```bash
pytest tests/ -v
```

#### Run Tests with Coverage

```bash
pytest --cov=custom_components/controllable --cov-report=html
open htmlcov/index.html  # View coverage report
```

#### Run Specific Test

```bash
pytest tests/test_switch.py -v
```

### 4. Code Quality Checks

#### Format Code

```bash
black custom_components/
isort custom_components/
```

#### Lint Code

```bash
# Check for style issues
flake8 custom_components/

# Type checking
mypy custom_components/

# Security scan
bandit -r custom_components/
```

### 5. Home Assistant Integration Testing

#### Using Docker Development Environment

```bash
# Start development environment
./dev.sh start

# Access Home Assistant at http://localhost:8123
```

#### Manual Testing

1. Copy `custom_components/controllable` to your HA config directory
2. Restart Home Assistant
3. Check logs for any errors:

```yaml
logger:
  default: info
  logs:
    custom_components.controllable: debug
```

## Controllable Integration Details

### Synchronization Logic

The integration creates virtual switches that proxy real entities:

- **State Mirroring**: Virtual switches reflect real entity states
- **Sync Tracking**: `is_synced` attribute monitors synchronization
- **Event Handling**: Listens for state changes to update sync status
- **Device Grouping**: Virtual entities added to target's device

### Configuration

- **Name**: Friendly name for virtual switch
- **Target Entity**: Real entity to proxy (switch/light/fan)

### Entities

- **Virtual Switch**: Controls real entity with sync protection
- **Attributes**: `is_synced`, `target_entity`
- **Device**: Added to target's device registry

## Contributing

### Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and add tests
4. Run all tests and quality checks
5. Commit your changes: `git commit -m 'Add some feature'`
6. Push to the branch: `git push origin feature/your-feature`
7. Open a Pull Request

### Code Standards

- **Python Version**: 3.12+
- **Formatting**: Black
- **Imports**: isort
- **Linting**: flake8
- **Types**: mypy
- **Testing**: pytest with coverage

### Commit Messages

Use conventional commit format:

```
feat: add new sync logic
fix: handle target entity changes
docs: update installation instructions
test: add tests for config flow
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Sync Issues**: Check target entity availability
3. **Device Registry**: Verify target has device
4. **HA Integration Issues**: Check Home Assistant logs

### Debug Logging

Enable debug logging in `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.controllable: debug
```

### Testing with Mock Entities

For development, create mock entities in HA to test sync behavior.
