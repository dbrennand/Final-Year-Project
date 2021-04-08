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


def get_env_vars(env_vars: list) -> dict:
    """Get a dictionary containing the provided environment variable(s) name(s) and value(s).

    Args:
        env_vars (list): A list of environment variable name(s) to retrieve the value(s) for.

    Raises:
        ValueError: Occurs when an environment variable value is None.

    Returns:
        dict: A dictionary containing the environment variable name(s) and value(s) as key value pairs.
    """
    # Initialise environment variable dictionary
    env_vars_dict = {}
    for env_var in env_vars:
        # Get environment variable value
        # Default to None if not found
        env_var_value = os.environ.get(env_var, None)
        # Check env_var_value is not None
        # If None, log error and raise ValueError
        if isinstance(env_var_value, None):
            log_message(
                message=f"Environment variable: {env_var} is missing. See prerequisite steps in the README file.",
                level="ERROR",
            )
            raise ValueError(
                f"Environment variable: {env_var} is missing. See prerequisite steps in the README file."
            )
        # Is present as a str
        else:
            # Add environment variable name and value to env_vars_dict
            env_vars_dict[env_var] = env_var_value
    return env_vars_dict


def get_api_creds() -> typing.Tuple[dict, str]:
    """Get API credentials from environment variables.

    Raises:
        ValueError: Occurs when one or more API credentials are missing.

    Returns:
        typing.Tuple[dict, str]: A tuple containing a dictionary and a string.
            Dictionary: Contains credentials for the Tweepy constructor.
            String: Contains the Botometer API key.
    """
    # Get API credentials from environment variables
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


def get_email_creds() -> typing.Tuple[str, str, int]:
    """Get email server credentials from environment variables.

    Raises:
        ValueError: Occurs when one or more email server credentials are missing.

    Returns:
        typing.Tuple[str, str, int]: A tuple containing two strings amd an integer.
            String 1: The email server domain name.
            String 2: The email server password.
            Integer: The email server port used to connect to the email server.
    """
    # Get email credentials from environment variables
    pass