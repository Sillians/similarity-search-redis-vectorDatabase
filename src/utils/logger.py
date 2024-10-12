import logging
import os
from datetime import datetime


# Create a logger
def get_logger(name: str, log_file: str = "similarity_search.log", level: int = logging.INFO) -> logging.Logger:
    """Initializes and returns a
    logger for reproducibility and traceability.
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent logger from propagating to the root logger
    logger.propagate = False

    # logging format
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # file handler to log to a file
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # stream handler to log to the console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


# Function to generate a unique log file name based on date and time
def get_unique_log_filename(base_name="log"):
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return f"{base_name}_{current_time}.log"


# Example of how to initialize and use the logger in another module
if __name__ == "__main__":
    log_file = get_unique_log_filename("similarity-search_log")
    logger = get_logger("example_logger", log_file)

    logger.info("This is an info message for tracking!")
    logger.error("This is an error message!")
