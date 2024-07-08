import logging
import os

def setup_logger(name, log_file, level=logging.INFO):
    """Function to set up a logger with a specified name, log file, and logging level."""
    
    # Ensure the log directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create handlers
    file_handler = logging.FileHandler(log_file)
    stream_handler = logging.StreamHandler()

    # Create formatters and add them to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
    return logger

# Example usage
if __name__ == "__main__":
    # Example configuration
    log_name = 'IoTResourceOptimizerLogger'
    log_file = 'logs/iot_resource_optimizer.log'
    log_level = logging.DEBUG
    
    # Set up the logger
    logger = setup_logger(log_name, log_file, log_level)
    
    # Log some messages
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')
