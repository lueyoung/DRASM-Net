import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import requests
import json
from utils.logger import setup_logger
from config.config import Config

class SDNController:
    def __init__(self, config):
        self.config = config
        self.logger = setup_logger('SDNControllerLogger', self.config.get('logging.log_file', 'logs/sdn_controller.log'))

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

    def manage_flow_table(self, flow_entries):
        """
        Manage the flow table by adding new flow entries.

        :param flow_entries: List of flow entries to be added to the flow table.
        """
        url = f"{self.base_url}/flowtable"
        headers = {'Content-Type': 'application/json'}

        for entry in flow_entries:
            try:
                response = requests.post(url, headers=headers, data=json.dumps(entry))
                response.raise_for_status()
                self.logger.info(f"Successfully added flow entry: {entry}")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error adding flow entry: {entry}, Error: {e}")

    def centralized_control(self):
        """
        Example method to demonstrate centralized control.
        """
        # Fetch current topology
        topology = self.get_topology()
        if topology:
            self.logger.info(f"Current topology: {json.dumps(topology, indent=4)}")
            # Example: Add a flow entry to control traffic
            example_flow_entry = {
                "switch": "00:00:00:00:00:00:00:01",
                "name": "flow_mod_1",
                "cookie": "0",
                "priority": "32768",
                "in_port": "1",
                "active": "true",
                "actions": "output=flood"
            }
            self.manage_flow_table([example_flow_entry])
        else:
            self.logger.error("Failed to fetch topology.")

    def get_topology(self):
        """
        Get the current network topology from the SDN controller.

        :return: Network topology as a dictionary, or None if the request fails.
        """
        url = f"{self.base_url}/topology"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching topology: {e}")
            return None

    def dynamic_resource_allocation(self, allocation_strategy):
        """
        Perform dynamic resource allocation based on a given strategy.

        :param allocation_strategy: A strategy dict defining resource allocation rules.
        """
        # Implement the allocation strategy logic
        # Example: Adjust flow entries based on the strategy
        flow_entries = self.generate_flow_entries_from_strategy(allocation_strategy)
        self.manage_flow_table(flow_entries)

    def generate_flow_entries_from_strategy(self, strategy):
        """
        Generate flow entries based on the provided strategy.

        :param strategy: A strategy dict defining resource allocation rules.
        :return: List of flow entries.
        """
        # Implement logic to generate flow entries from strategy
        flow_entries = []
        for rule in strategy.get('rules', []):
            entry = {
                "switch": rule.get("switch"),
                "name": rule.get("name"),
                "cookie": rule.get("cookie", "0"),
                "priority": rule.get("priority", "32768"),
                "in_port": rule.get("in_port"),
                "active": rule.get("active", "true"),
                "actions": rule.get("actions")
            }
            flow_entries.append(entry)
        return flow_entries

# Example usage
if __name__ == "__main__":
    # Load configuration
    config = Config(config_file='config/config.json')

    # Initialize SDN Controller with configuration
    sdn_controller = SDNController(config=config)

    # Demonstrate centralized control
    sdn_controller.centralized_control()

    # Example strategy for dynamic resource allocation
    allocation_strategy = {
        "rules": [
            {
                "switch": "00:00:00:00:00:00:00:01",
                "name": "dynamic_flow_1",
                "priority": "40000",
                "in_port": "2",
                "actions": "output=3"
            },
            {
                "switch": "00:00:00:00:00:00:00:02",
                "name": "dynamic_flow_2",
                "priority": "40000",
                "in_port": "3",
                "actions": "output=2"
            }
        ]
    }

    # Perform dynamic resource allocation
    sdn_controller.dynamic_resource_allocation(allocation_strategy)
