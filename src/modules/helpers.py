"""Module containing helper functions for the application.
"""
import loguru
import os
import typing

# Logging functions


def check_log_record_level(record: dict) -> typing.Tuple[bool, None]:
    """A loguru filter to check each log record's level.

    If the log record's level is "ERROR", then terminate the application.
    Otherwise, return True, returning the log record back to the configured handler.

    https://github.com/Delgan/loguru/issues/425

    Args:
        record (dict): A log record containing metadata.

    Returns:
        typing.Tuple[bool, None]: Returns a boolean of True or None.
            Returns True when the log record level is not "ERROR".
            Returns None when the log record level is "ERROR". Application terminates.
    """
    if record["level"].name == "ERROR":
        exit()
    return True


def init_log_handler() -> None:
    """Initialise a log handler using loguru.

    Adds a log handler with a sink to handle log messages.
    By default, loguru adds a sink to stderr. This also configures a sink to send logs to a file.

    https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.add

    Returns:
        None.
    """
    # Add a log handler to send log messages to a file
    # Specify formatting, filtering and other parameters
    # Diagnose is False to prevent leak of credentials in production
    loguru.logger.add(
        sink="app_{time}.log",
        format="{time:DD:MM:YYYY - HH:mm:ss} | {level} | {file}:{name}:{line} - {message}",
        filter=check_log_record_level,
        backtrace=True,
        diagnose=False,
    )


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
    loguru.logger.info(f"Getting environment variables: {env_vars}")
    # Initialise environment variable dictionary
    env_vars_dict = {}
    for env_var in env_vars:
        # Get environment variable value
        # Default to None if not found
        env_var_value = os.environ.get(env_var, None)
        # Check env_var_value is not None
        # If None log error
        if isinstance(env_var_value, None):
            loguru.logger.exception(
                f"Environment variable: {env_var} is missing. See prerequisite steps in the README file."
            )
        # Is present as a str
        else:
            loguru.logger.debug(
                f"Environment variable: {env_var} found. Adding to dictionary."
            )
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
    loguru.logger.info("Getting API credentials.")
    # Get Twitter and Botometer API credentials from environment variables
    api_env_dict = get_env_vars(
        ["TWITTER_API_KEY", "TWITTER_API_SECRET", "BOTOMETER_API_KEY"]
    )
    # Create dictionary containing credentials for Tweepy constructor
    twitter_api_creds = {
        "consumer_key": api_env_dict["TWITTER_API_KEY"],
        "consumer_secret": api_env_dict["TWITTER_API_SECRET"],
    }
    # Create dictionary containing credentials for Botometer constructor
    botometer_api_creds = {
        "rapidapi_key": api_env_dict["BOTOMETER_API_KEY"],
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
    loguru.logger.info("Getting email credentials.")
    # Get email credentials from environment variables
    return get_env_vars(
        [
            "EMAIL_SERVER_DOMAIN",
            "EMAIL_SERVER_PORT",
            "EMAIL_SENDER_ADDRESS",
            "EMAIL_SENDER_PASSWORD",
        ]
    )
