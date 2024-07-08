import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import numpy as np
from utils.logger import setup_logger

class StabilityAnalysis:
    def __init__(self, config):
        self.config = config
        self.logger = setup_logger('StabilityAnalysisLogger', self.config.get('logging.log_file', 'logs/stability_analysis.log'))
        self.epsilon = self.config.get('stability_analysis.epsilon', 1e-5)
        self.alpha = self.config.get('stability_analysis.alpha', 0.1)

    def lyapunov_function(self, traffic_intensities, equilibrium_intensity):
        """
        Define the Lyapunov function for stability analysis.

        :param traffic_intensities: List of traffic intensities ?i for each node.
        :param equilibrium_intensity: Equilibrium traffic intensity ?0.
        :return: Value of the Lyapunov function.
        """
        return np.sum((traffic_intensities - equilibrium_intensity) ** 2)

    def lyapunov_derivative(self, traffic_intensities, perturbations):
        """
        Compute the derivative of the Lyapunov function.

        :param traffic_intensities: List of traffic intensities ?i for each node.
        :param perturbations: Perturbations ??i and ?µi for each node.
        :return: Value of the derivative of the Lyapunov function.
        """
        equilibrium_intensity = np.mean(traffic_intensities)
        return 2 * np.sum((traffic_intensities - equilibrium_intensity) * perturbations)

    def stability_analysis(self, arrival_rates, service_rates):
        """
        Perform stability analysis using Lyapunov's direct method.

        :param arrival_rates: List of arrival rates ?i for each node.
        :param service_rates: List of service rates µi for each node.
        :return: Boolean indicating system stability.
        """
        traffic_intensities = arrival_rates / service_rates
        equilibrium_intensity = np.mean(traffic_intensities)

        # Small perturbations ??i and ?µi
        perturbations = np.random.normal(0, self.epsilon, len(arrival_rates))
        traffic_intensities_perturbed = traffic_intensities + perturbations

        V = self.lyapunov_function(traffic_intensities, equilibrium_intensity)
        V_dot = self.lyapunov_derivative(traffic_intensities, traffic_intensities_perturbed - traffic_intensities)

        self.logger.info(f"Lyapunov function V: {V}")
        self.logger.info(f"Lyapunov derivative V_dot: {V_dot}")

        return V_dot < 0

    def analyze(self, allocation_strategy):
        """
        Analyze stability for a given resource allocation strategy.

        :param allocation_strategy: A strategy dict defining resource allocation rules.
        :return: Boolean indicating overall system stability.
        """
        arrival_rates = np.array(allocation_strategy['arrival_rates'])
        service_rates = self.alpha * np.array(allocation_strategy['allocations'])

        return self.stability_analysis(arrival_rates, service_rates)

# Example usage
if __name__ == "__main__":
    # Example configuration
    config_data = {
        "stability_analysis": {
            "epsilon": 1e-5,
            "alpha": 0.1
        },
        "logging": {
            "log_file": "logs/stability_analysis.log",
            "log_level": "DEBUG"
        }
    }

    # Initialize Stability Analysis with configuration
    stability_analyzer = StabilityAnalysis(config=config_data)

    # Example allocation strategy
    allocation_strategy = {
        "arrival_rates": [10, 20, 30, 40],
        "allocations": [100, 200, 300, 400]
    }

    # Perform stability analysis
    is_stable = stability_analyzer.analyze(allocation_strategy)
    print(f"System is stable: {is_stable}")
