import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import requests
import json
from utils.logger import setup_logger
from config.config import Config

class NetworkMonitor:
    def __init__(self, config):
        self.config = config
        self.logger = setup_logger('NetworkMonitorLogger', self.config.get('logging.log_file', 'logs/network_monitor.log'))
        self.base_url = f"{self.config.get('network.protocol')}://{self.config.get('network.host')}:{self.config.get('network.port')}"

    def get_network_status(self):
        """
        Get the current status of the network including traffic and node statuses.

        :return: Network status as a dictionary.
        """
        url = f"{self.base_url}/network/status"
        try:
            response = requests.get(url)
            response.raise_for_status()
            network_status = response.json()
            self.logger.info(f"Network status: {json.dumps(network_status, indent=4)}")
            return network_status
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching network status: {e}")
            raise ValueError("Failed to fetch network status.")

    def monitor_traffic(self):
        """
        Monitor network traffic and return traffic statistics.

        :return: Traffic statistics as a dictionary.
        """
        url = f"{self.base_url}/network/traffic"
        try:
            response = requests.get(url)
            response.raise_for_status()
            traffic_stats = response.json()
            self.logger.info(f"Traffic statistics: {json.dumps(traffic_stats, indent=4)}")
            return traffic_stats
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching traffic statistics: {e}")
            raise ValueError("Failed to fetch traffic statistics.")

    def monitor_congestion(self):
        """
        Monitor network congestion and return congestion metrics.

        :return: Congestion metrics as a dictionary.
        """
        url = f"{self.base_url}/network/congestion"
        try:
            response = requests.get(url)
            response.raise_for_status()
            congestion_metrics = response.json()
            self.logger.info(f"Congestion metrics: {json.dumps(congestion_metrics, indent=4)}")
            return congestion_metrics
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching congestion metrics: {e}")
            raise ValueError("Failed to fetch congestion metrics.")

# Example usage
if __name__ == "__main__":
    # Example configuration
    config_data = {
        "resource_allocation": {
            "total_resources": 1000,
            "alpha": 0.1,
            "beta": 0.1,
            "gamma": 0.1,
            "epsilon": 1e-5,
            "max_iterations": 100
        },
        "logging": {
            "log_file": "logs/network_manager.log",
            "log_level": "DEBUG"
        }
    }
    network_config = {
        "protocol": "http",
        "host": "localhost",
        "port": 8080
    }

    # Initialize Network Monitor with configuration
    network_monitor = NetworkMonitor(config=config_data)

    # Monitor network status
    network_status = network_monitor.get_network_status()
    print(f"Network Status: {network_status}")

    # Monitor traffic statistics
    traffic_stats = network_monitor.monitor_traffic()
    print(f"Traffic Statistics: {traffic_stats}")

    # Monitor congestion metrics
    congestion_metrics = network_monitor.monitor_congestion()
    print(f"Congestion Metrics: {congestion_metrics}")
