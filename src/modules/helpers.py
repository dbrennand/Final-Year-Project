"""Module containing helper functions for the application.
"""
import loguru
import os
import typing
import datetime
import pycountry
import jinja2

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
    Furthermore, the logger is application wide meaning log calls can be made anywhere
    as long as loguru is imported.

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


def get_datetime() -> str:
    """Get the current datetime as a formatted string.

    NOTE: The datetime library uses the operating system's configured timezone.

    Returns:
        str: A string formatted like: "05/04/2021 at 13:04:15".
    """
    loguru.logger.debug("Getting current datetime.")
    return datetime.datetime.now().strftime("%d/%m/%Y at %H:%M:%S")


def get_lang_from_code(lang_code: str) -> str:
    """Get language name from an ISO 639-1 language code.

    Args:
        lang_code (str): A language code in ISO 639-1 format.
            Examples: "en", "de".

    Returns:
        str: The name of the language if successfully retrieved. Otherwise, returns "Unknown".
    """
    # Lookup language using ISO 639-1 language code provided by the Botometer API
    language = pycountry.languages.get(alpha_2=lang_code)
    # Check a language has been returned
    if language:
        # Get language name and return it
        return language.name
    # If not, return "Unknown"
    else:
        return "Unknown"


# Report functions


def render_report(
    username: str,
    friends_bot_likelihood_scores: list,
    template_dir: str = f"{os.getcwd()}/src/template",
) -> str:
    """Render the friends bot likelihood report from a template using the Jinja2 templating engine.

    Notes:
        The report is structured and styled using HTML and CSS.
        The email template is located at: /src/template/report_template.html.

    Args:
        username (str): The username of the Twitter account the report has been generated for.
        friends_bot_likelihood_scores (list): A list of bot likelihood scores from the Botometer API for Twitter friends.
        template_dir (str, optional): The directory to look for the report template. Defaults to "{os.getcwd()}/src/template".

    Returns:
        str: A unicode formatted string of the rendered report.
    """
    # Create template loader
    template_loader = jinja2.FileSystemLoader(template_dir)
    # Create template environment
    environment = jinja2.Environment(loader=template_loader)
    # Get the report template
    report_template = environment.get_template(name="report_template.html")
    # Get datetime formatted string to be provided to the template
    datetime_str = get_datetime()
    # Render report from template
    # Providing data to be used in the template
    loguru.logger.info("Rendering report from template.")
    report_render = report_template.render(
        username=username,
        friends_bot_likelihood_scores=friends_bot_likelihood_scores,
        datetime_str=datetime_str,
    )
    return report_render


def dump_report(
    report_render: str, username: str, dump_dir: str = f"{os.getcwd()}/src/reports"
) -> None:
    """Dump the rendered friends bot likelihood report to a file.

    Args:
        report_render (str): A unicode formatted string of the rendered report.
        username (str): The username of the Twitter account the report has been generated for.
        dump_dir (str, optional): The directory to dump the report to. Defaults to f"{os.getcwd()}/src/reports".

    Returns:
        None.
    """
    # Check if the reports directory exists, if not create it
    if not os.path.exists(dump_dir):
        loguru.logger.debug("Reports directory does not exist. Creating...")
        try:
            os.mkdir(dump_dir)
        except OSError as err:
            # If an error occurs here, dump the report str and terminate the application
            loguru.logger.debug(f"Report render dump:\n{report_render}")
            loguru.logger.exception(
                f"An exception occurred when creating reports directory at path: {dump_dir}\n{err}"
            )
    else:
        loguru.logger.debug("Reports directory already exists.")
    # Create report full path
    report_file_path = f"{dump_dir}/@{username}_friends_report.html"
    # Dump the report render to a file in the reports directory
    try:
        with open(report_file_path, "w") as report_file:
            report_file.write(report_render)
    except OSError as err:
        loguru.logger.debug(f"Report render dump:\n{report_render}")
        loguru.logger.exception(
            f"An exception occurred when writing report render to file: {report_file_path}\n{err}"
        )
