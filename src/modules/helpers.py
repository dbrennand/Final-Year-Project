"""Helper functions for the application.
"""
import loguru

# Logging functions


def init_logger() -> None:
    """Initialise logging to stdout and a file for the application.

    Returns:
        None.
    """
    # Initialise logger to stdout and a file with specific formatting
    loguru.logger.add("app_{time}.log", format="{time} {level} {message}")


def log_message(message: str, level: str = "INFO") -> None:
    """Log a message to stdout and the log file.

    Args:
        message (str): The log message.
        level (str, optional): The log level for the message. Defaults to "INFO".

    Returns:
        None.
    """
    loguru.logger.log(level, message)
