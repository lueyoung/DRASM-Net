import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import numpy as np
from scipy.optimize import minimize
from utils.logger import setup_logger

class ResourceAllocation:
    def __init__(self, config):
        self.config = config
        self.logger = setup_logger('ResourceAllocationLogger', self.config.get('logging.log_file', 'logs/resource_allocation.log'))
        self.total_resources = self.config.get('resource_allocation.total_resources', 1000)
        self.alpha = self.config.get('resource_allocation.alpha', 0.1)
        self.beta = self.config.get('resource_allocation.beta', 0.1)
        self.gamma = self.config.get('resource_allocation.gamma', 0.1)
        self.epsilon = self.config.get('resource_allocation.epsilon', 1e-5)
        self.max_iterations = self.config.get('resource_allocation.max_iterations', 100)

    def allocate_resources(self, arrival_rates, priority_levels, initial_allocations=None):
        """
        Allocate resources dynamically based on arrival rates and priority levels.

        :param arrival_rates: List of arrival rates ?i for each node.
        :param priority_levels: List of priority levels Pij for each node.
        :param initial_allocations: Initial resource allocations (optional).
        :return: Optimal resource allocations for each node.
        """
        num_nodes = len(arrival_rates)
        if initial_allocations is None:
            initial_allocations = np.full(num_nodes, self.total_resources / num_nodes)

        def objective(R):
            delay = sum(arrival_rates[i] * (1 / (self.alpha * R[i]) + self.beta * priority_levels[i]) for i in range(num_nodes))
            utilization = sum(self.gamma * (self.total_resources - R[i]) for i in range(num_nodes))
            return delay + utilization

        constraints = [
            {'type': 'eq', 'fun': lambda R: np.sum(R) - self.total_resources},
            {'type': 'ineq', 'fun': lambda R: R - np.zeros(num_nodes)},  # R >= 0
            {'type': 'ineq', 'fun': lambda R: np.ones(num_nodes) - (arrival_rates / (self.alpha * R))}  # ?i < 1
        ]

        result = minimize(objective, initial_allocations, constraints=constraints, options={'maxiter': self.max_iterations})

        if not result.success:
            self.logger.error(f"Optimization failed: {result.message}")
            raise ValueError("Resource allocation optimization failed.")

        optimal_allocations = result.x
        self.logger.info(f"Optimal resource allocations: {optimal_allocations}")
        return optimal_allocations

    def stability_analysis(self, arrival_rates, resource_allocations):
        """
        Perform stability analysis using Lyapunov's direct method.

        :param arrival_rates: List of arrival rates ?i for each node.
        :param resource_allocations: List of resource allocations Ri for each node.
        :return: Boolean indicating system stability.
        """
        traffic_intensities = arrival_rates / (self.alpha * resource_allocations)
        equilibrium_intensity = np.mean(traffic_intensities)

        def lyapunov_function(rho):
            return np.sum((rho - equilibrium_intensity) ** 2)

        def lyapunov_derivative(rho, delta_rho):
            return 2 * np.sum((rho - equilibrium_intensity) * delta_rho)

        perturbations = np.random.normal(0, self.epsilon, len(arrival_rates))
        rho_perturbed = traffic_intensities + perturbations

        V = lyapunov_function(traffic_intensities)
        V_dot = lyapunov_derivative(traffic_intensities, rho_perturbed - traffic_intensities)

        self.logger.info(f"Lyapunov function V: {V}")
        self.logger.info(f"Lyapunov derivative V_dot: {V_dot}")

        return V_dot < 0

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
            "log_file": "logs/resource_allocation.log",
            "log_level": "DEBUG"
        }
    }

    # Initialize Resource Allocation with configuration
    resource_allocator = ResourceAllocation(config=config_data)

    # Example arrival rates and priority levels
    arrival_rates = np.array([10, 20, 30, 40])
    priority_levels = np.array([1, 2, 3, 4])

    # Perform resource allocation
    optimal_allocations = resource_allocator.allocate_resources(arrival_rates, priority_levels)

    # Perform stability analysis
    is_stable = resource_allocator.stability_analysis(arrival_rates, optimal_allocations)
    print(f"System is stable: {is_stable}")
