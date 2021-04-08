"""Module containing helper functions for the application.
"""
import loguru
import os
import typing

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


# Utility functions


def get_api_creds() -> typing.Tuple[dict, str]:
    """Get API credentials from environment variables.

    Raises:
        ValueError: Occurs when one or more API credentials are missing.

    Returns:
        typing.Tuple[dict, str]: A tuple containing a dictionary and a string.
            Dictionary: Contains credentials for the Tweepy constructor.
            String: Contains the Botometer API key.
    """
    # Obtain API credentials from environment variables
    # Twitter API credentials
    twitter_api_key = os.environ.get("TWITTER_API_KEY", None)
    titter_api_secret = os.environ.get("TWITTER_API_SECRET", None)
    # Botometer (Rapid) API key
    botometer_api_key = os.environ.get("BOTOMETER_API_KEY", None)
    # Check API credentials are not None
    # If None, log error and raise ValueError
    if not all([twitter_api_key, twitter_api_secret, botometer_api_key]):
        log_message(
            message="One or more API credentials are missing. Provide the environment variables: TWITTER_API_KEY, TWITTER_API_SECRET and BOTOMETER_API_KEY.",
            level="ERROR",
        )
        raise ValueError(
            "One or more API credentials are missing. See usage heading in the README file."
        )
    # Return a tuple containing a dictionary and string
    # Dictionary contains credentials for the Tweepy constructor and the string is the Botometer API key
    # Only returning the Botometer API key because Botometer also requires the Twitter API credentials in its constructor
    twitter_auth = {
        "consumer_key": twitter_api_key,
        "consumer_secret": twitter_api_secret,
    }
    return twitter_auth, botometer_api_key
