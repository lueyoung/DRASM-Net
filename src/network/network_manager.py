import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import requests
import json
from utils.logger import setup_logger
from config.config import Config

class NetworkManager:
    def __init__(self, config):
        self.config = config
        self.logger = setup_logger('NetworkManagerLogger', self.config.get('logging.log_file', 'logs/network_manager.log'))
        
        # Retrieve network settings
        self.protocol = self.config.get('network.protocol')
        self.host = self.config.get('network.host')
        self.port = self.config.get('network.port')
        
        # Debugging: Print retrieved settings
        self.logger.debug(f"Protocol: {self.protocol}, Host: {self.host}, Port: {self.port}")

        # Construct the base URL
        self.base_url = f"{self.protocol}://{self.host}:{self.port}"
        
        # Debugging: Print constructed base URL
        self.logger.debug(f"Base URL: {self.base_url}")

    def configure_network(self, network_config):
        """
        Configure the network based on the provided configuration.

        :param network_config: Configuration settings for the network.
        """
        url = f"{self.base_url}/network/configure"
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(network_config))
            response.raise_for_status()
            self.logger.info(f"Successfully configured the network with config: {network_config}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error configuring the network: {e}")
            raise ValueError("Network configuration failed.")

    def manage_nodes(self, nodes):
        """
        Manage network nodes by adding, removing, or updating node configurations.

        :param nodes: List of node configurations.
        """
        url = f"{self.base_url}/network/nodes"
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.put(url, headers=headers, data=json.dumps(nodes))
            response.raise_for_status()
            self.logger.info(f"Successfully managed network nodes: {nodes}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error managing network nodes: {e}")
            raise ValueError("Network node management failed.")

    def allocate_resources(self, resource_allocation):
        """
        Allocate network resources dynamically.

        :param resource_allocation: Resource allocation settings.
        """
        url = f"{self.base_url}/network/resources"
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(resource_allocation))
            response.raise_for_status()
            self.logger.info(f"Successfully allocated resources: {resource_allocation}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error allocating resources: {e}")
            raise ValueError("Resource allocation failed.")

    def monitor_network(self):
        """
        Monitor network status and return the current state.

        :return: Current network status.
        """
        url = f"{self.base_url}/network/status"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            network_status = response.json()
            self.logger.info(f"Current network status: {network_status}")
            return network_status
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error monitoring network: {e}")
            raise ValueError("Network monitoring failed.")

# Example usage
if __name__ == "__main__":
    # Load configuration
    config = Config(config_file='config/config.json')
    
    # Initialize Network Manager with configuration
    network_manager = NetworkManager(config=config)
    
    # Example network configuration
    network_configuration = {
        "switches": [
            {"id": "00:00:00:00:00:00:00:01", "ports": 4},
            {"id": "00:00:00:00:00:00:00:02", "ports": 4}
        ],
        "links": [
            {"source": "00:00:00:00:00:00:00:01", "destination": "00:00:00:00:00:00:00:02", "capacity": 1000}
        ]
    }
    
    # Configure the network
    network_manager.configure_network(network_configuration)
    
    # Example nodes management
    nodes = [
        {"id": "00:00:00:00:00:00:00:01", "action": "add"},
        {"id": "00:00:00:00:00:00:00:02", "action": "add"}
    ]
    
    # Manage network nodes
    network_manager.manage_nodes(nodes)
    
    # Example resource allocation
    resource_allocation = {
        "resources": [
            {"id": "00:00:00:00:00:00:00:01", "allocated": 500},
            {"id": "00:00:00:00:00:00:00:02", "allocated": 500}
        ]
    }
    
    # Allocate resources
    network_manager.allocate_resources(resource_allocation)
    
    # Monitor network
    network_status = network_manager.monitor_network()
    print(f"Network Status: {network_status}")
