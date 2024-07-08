import json
import os

class Config:
    def __init__(self, config_file=None):
        self.config = {}
        self.load_default_config()
        if config_file:
            self.load_config_from_file(config_file)

    def load_default_config(self):
        # Define default configuration settings
        self.config = {
            "network": {
                "host": "localhost",
                "port": 8080,
                "protocol": "http"
            },
            "resource_allocation": {
                "initial_allocation": 100,
                "max_allocation": 1000,
                "allocation_step": 10
            },
            "stability_analysis": {
                "stability_threshold": 0.01,
                "max_iterations": 100
            },
            "logging": {
                "log_file": "iot_resource_optimizer.log",
                "log_level": "INFO"
            }
        }

    def load_config_from_file(self, config_file):
        try:
            with open(config_file, 'r') as file:
                file_config = json.load(file)
                self.update_config(file_config)
        except FileNotFoundError:
            print(f"Config file {config_file} not found. Using default configuration.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from the config file {config_file}. Using default configuration.")

    def update_config(self, new_config):
        self._update_recursive(self.config, new_config)

    def _update_recursive(self, original, new):
        for key, value in new.items():
            if isinstance(value, dict) and key in original:
                self._update_recursive(original[key], value)
            else:
                original[key] = value

    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        try:
            for k in keys:
                value = value[k]
        except KeyError:
            return default
        return value

# Example usage
if __name__ == "__main__":
    # Load configuration with a specific config file
    config = Config(config_file='config.json')
    
    # Get specific configuration values
    network_host = config.get('network.host')
    resource_initial_allocation = config.get('resource_allocation.initial_allocation')
    
    # Print configuration values
    print(f"Network Host: {network_host}")
    print(f"Initial Resource Allocation: {resource_initial_allocation}")
    
    # Update configuration dynamically
    config.update_config({
        "network": {
            "host": "127.0.0.1"
        },
        "logging": {
            "log_level": "DEBUG"
        }
    })
    
    # Print updated configuration values
    updated_network_host = config.get('network.host')
    updated_log_level = config.get('logging.log_level')
    print(f"Updated Network Host: {updated_network_host}")
    print(f"Updated Log Level: {updated_log_level}")
