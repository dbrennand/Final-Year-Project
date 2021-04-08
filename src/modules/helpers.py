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


def get_api_creds() -> typing.Tuple[dict, dict]:
    """Get API credentials for the Tweepy and Botometer constructors.

    Returns:
        typing.Tuple[dict, dict]: A tuple containing two dictionaries.
            Dictionary 1: Contains credentials for the Tweepy constructor.
            Dictionary 2: Contains credentials for the Botometer constructor.

    Note:
        Each dictionary can be passed directly to the constructor.
    """
    # Get Twitter and Botometer API credentials from environment variables
    api_env_dict = get_env_vars(["TWITTER_API_KEY", "TWITTER_API_SECRET", "BOTOMETER_API_KEY"])
    # Create dictionary containing credentials for Tweepy constructor
    twitter_api_creds = {
        "consumer_key": api_env_dict["TWITTER_API_KEY"],
        "consumer_secret": api_env_dict["TWITTER_API_SECRET"],
    }
    # Create dictionary containing credentials for Botometer constructor
    botometer_api_creds = {
        "rapidapi_key": api_env_dict["BOTOMETER_API_KEY"]
        "consumer_key": api_env_dict["TWITTER_API_KEY"],
        "consumer_secret": api_env_dict["TWITTER_API_SECRET"],
    }
    # Return a tuple containing the two dictionaries
    return twitter_api_creds, botometer_api_creds


def get_email_creds() -> dict:
    """Get email credentials for smtplib.

    Returns:
        dict: A dictionary containing the email credentials.
    """
    # Get email credentials from environment variables
    return get_env_vars(["EMAIL_SERVER_DOMAIN", "EMAIL_SERVER_PORT", "EMAIL_SENDER_ADDRESS", "EMAIL_SENDER_PASSWORD"])
