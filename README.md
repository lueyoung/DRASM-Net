### README.md

# DRASM-Net

The DRASM-Net is a system designed to optimize resource allocation in an IoT network using an SDN (Software-Defined Networking) approach. This project includes various components such as a POX controller, Mininet for network emulation, and a main application that performs resource allocation and stability analysis.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Components](#components)
- [Configuration](#configuration)
- [Logging](#logging)
- [Scripts](#scripts)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.6, 3.7, 3.8, or 3.9
- POX SDN Controller
- Mininet
- Git

### Steps

1. **Clone the Repository**

   ```sh
   git clone https://github.com/lueyoung/DRASM-Net.git
   cd DRASM-Net
   ```

2. **Install Dependencies**

   Ensure you have the required Python packages installed:

   ```sh
   pip install -r requirements.txt
   ```

3. **Set Up POX**

   Ensure POX is installed and accessible:

   ```sh
   git clone https://github.com/noxrepo/pox.git
   ```

   Setup REST API:

   ```sh
   cp DRASM-Net/src/ext/rest_api.py YOUR_POX_DIR/ext/
   ```

## Usage

### Starting the System

To start the IoT Resource Optimizer system, run the `start.sh` script:

```sh
./scripts/start.sh
```

### Stopping the System

To stop the IoT Resource Optimizer system, run the `stop.sh` script:

```sh
./scripts/stop.sh
```

## Components

- **POX Controller**: Manages the SDN network and provides a REST API for network configuration and monitoring.
- **Mininet**: Emulates the network topology.
- **Main Application**: Performs resource allocation, stability analysis, and network monitoring.

## Configuration

The system configuration is specified in `src/config/config.json`. Update this file to change the network settings, resource allocation parameters, and logging settings.

### Example Configuration (`src/config/config.json`)

```json
{
    "network": {
        "protocol": "http",
        "host": "localhost",
        "port": 8080
    },
    "resource_allocation": {
        "total_resources": 1000,
        "alpha": 0.1,
        "beta": 0.1,
        "gamma": 0.1,
        "epsilon": 1e-5,
        "max_iterations": 100
    },
    "stability_analysis": {
        "epsilon": 1e-5,
        "alpha": 0.1
    },
    "logging": {
        "log_file": "logs/main.log",
        "log_level": "DEBUG"
    }
}
```

## Logging

Logs are stored in the `logs` directory. Each component has its own log file:

- Main application: `logs/main.log`
- SDN Controller: `logs/sdn_controller.log`
- Resource Allocation: `logs/resource_allocation.log`
- Stability Analysis: `logs/stability_analysis.log`
- Network Manager: `logs/network_manager.log`
- Network Monitor: `logs/network_monitor.log`

## Scripts

### `scripts/start.sh`

This script starts the entire IoT Resource Optimizer system, including the POX controller, Mininet, and the main application.

### `scripts/stop.sh`

This script stops all components of the IoT Resource Optimizer system.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
