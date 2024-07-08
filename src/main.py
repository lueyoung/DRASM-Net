import sys
from config.config import Config
from utils.logger import setup_logger
from controllers.sdn_controller import SDNController
from algorithms.resource_allocation import ResourceAllocation
from algorithms.stability_analysis import StabilityAnalysis
from network.network_manager import NetworkManager
from network.network_monitor import NetworkMonitor

def main(config_file):
    # Load configuration
    config = Config(config_file=config_file)
    
    # Setup logger
    logger = setup_logger('MainLogger', config.get('logging.log_file', 'logs/main.log'))
    logger.info("Starting the IoT Resource Optimizer system...")

    # Initialize components
    sdn_controller = SDNController(config=config)
    resource_allocator = ResourceAllocation(config=config)
    stability_analyzer = StabilityAnalysis(config=config)
    network_manager = NetworkManager(config=config)
    network_monitor = NetworkMonitor(config=config)

    # Example configuration and allocation strategy
    network_configuration = {
        "switches": [
            {"id": "00:00:00:00:00:00:00:01", "ports": 4},
            {"id": "00:00:00:00:00:00:00:02", "ports": 4}
        ],
        "links": [
            {"source": "00:00:00:00:00:00:00:01", "destination": "00:00:00:00:00:00:00:02", "capacity": 1000}
        ]
    }
    allocation_strategy = {
        "arrival_rates": [10, 20, 30, 40],
        "allocations": [100, 200, 300, 400]
    }

    try:
        # Configure the network
        network_manager.configure_network(network_configuration)
        
        # Manage network nodes
        nodes = [
            {"id": "00:00:00:00:00:00:00:01", "action": "add"},
            {"id": "00:00:00:00:00:00:00:02", "action": "add"}
        ]
        network_manager.manage_nodes(nodes)
        
        # Allocate resources
        optimal_allocations = resource_allocator.allocate_resources(
            arrival_rates=allocation_strategy['arrival_rates'],
            priority_levels=[1, 2, 3, 4]
        )
        
        # Perform stability analysis
        is_stable = stability_analyzer.stability_analysis(
            arrival_rates=allocation_strategy['arrival_rates'],
            service_rates=optimal_allocations
        )
        
        # Log stability status
        logger.info(f"System stability status: {'Stable' if is_stable else 'Unstable'}")
        
        # Monitor network
        network_status = network_monitor.get_network_status()
        traffic_stats = network_monitor.monitor_traffic()
        congestion_metrics = network_monitor.monitor_congestion()
        
        # Log network status
        logger.info(f"Network Status: {network_status}")
        logger.info(f"Traffic Statistics: {traffic_stats}")
        logger.info(f"Congestion Metrics: {congestion_metrics}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

    logger.info("IoT Resource Optimizer system completed successfully.")

if __name__ == "__main__":
    # Ensure a config file is provided
    if len(sys.argv) != 2:
        print("Usage: python main.py <config_file>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    main(config_file)
