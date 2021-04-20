"""Module containing helper functions for the application.
"""
import loguru
import os
import typing
import datetime
import pycountry
import jinja2
import smtplib
import ssl

# Explicitly declare email imports
from email import encoders

# Due to -> AttributeError: module 'email' has no attribute 'mime'
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

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
        if env_var_value is not None:
            # Is present as a str
            loguru.logger.debug(
                f"Environment variable: {env_var} found. Adding to dictionary."
            )
            # Add environment variable name and value to env_vars_dict
            env_vars_dict[env_var] = env_var_value
        else:
            loguru.logger.exception(
                f"Environment variable: {env_var} is missing. See prerequisite steps in the README file."
            )
    return env_vars_dict


def get_datetime() -> str:
    """Get the current datetime as a formatted string.

    NOTE: The datetime library uses the operating system's configured timezone.

    Returns:
        str: A string formatted with the current date and time like: "05/04/2021 at 13:04:15".
    """
    loguru.logger.info("Getting current datetime string.")
    datetime_str = datetime.datetime.now().strftime("%d/%m/%Y at %H:%M:%S")
    loguru.logger.debug(f"Datetime string: {datetime_str}")
    return datetime_str


def get_lang_from_code(lang_code: str) -> str:
    """Get language name from an ISO 639-1 language code.

    Args:
        lang_code (str): A language code in ISO 639-1 format.
            Examples: "en", "de".

    Returns:
        str: The name of the language if available. Otherwise, returns "Unknown".
    """
    loguru.logger.info(f"Getting language name for code: {lang_code}")
    # Lookup language using ISO 639-1 language code provided by the Botometer API
    language = pycountry.languages.get(alpha_2=lang_code)
    # Check a language has been returned
    if language:
        # Get language name and return it
        language_name = language.name
        loguru.logger.debug(f"Got language name: {language_name}")
        return language.name
    # If not, return "Unknown"
    else:
        loguru.logger.debug(f"Language name for code: {lang_code} is unknown.")
        return "Unknown"


def create_reports_dir(reports_dir: str = f"{os.getcwd()}/src/reports") -> str:
    """Create a directory called "reports" to store the friends bot likelihood report(s).

    NOTE: This function is called in `dump_report`.

    Args:
        reports_dir (str, optional): The absolute or relative path to the reports
            directory to be created. Defaults to f"{os.getcwd()}/src/reports".

    Returns:
        str: The absolute or relative path to the reports directory.
    """
    # Check if the reports directory exists, if not create it
    if not os.path.exists(reports_dir):
        loguru.logger.debug(
            f"Reports directory at path: {reports_dir} does not exist. Creating..."
        )
        try:
            os.mkdir(reports_dir)
        except FileNotFoundError as err:
            loguru.logger.exception(
                f"Failed to create reports directory at path: {reports_dir}.\n{err}"
            )
    else:
        loguru.logger.debug(f"Reports directory at path: {reports_dir} already exists.")
    return reports_dir


def check_list_populated(_list: list) -> bool:
    """Check whether a list contains one or more items.

    Args:
        _list (list): A list to check whether it contains one or more items.

    Returns:
        bool: Returns True if the list has one or more items. Otherwise, returns False.
    """
    loguru.logger.debug("Checking if the list provided has one or more items.")
    # If the list is empty it will return False
    # Otherwise, returns True
    return bool(_list)


# Report functions


def render_report(
    username: str,
    friends_bot_likelihood_scores: list,
    datetime_str: str,
    template_dir: str = f"{os.getcwd()}/src/template",
) -> str:
    """Render the friends bot likelihood report from a template using the Jinja2 templating engine.

    Notes:
        The report is structured and styled using HTML and CSS.
        The email template is located at: /src/template/report_template.html.

    Args:
        username (str): The username of the Twitter account the report has been generated for.
        friends_bot_likelihood_scores (list): A list of bot likelihood scores from the Botometer API for Twitter friends.
        datetime_str (str): A string containing the current date and time (see get_datetime() function).
        template_dir (str, optional): The directory to look for the report template. Defaults to "{os.getcwd()}/src/template".

    Returns:
        str: A unicode formatted string of the rendered report.
    """
    # Create template loader
    template_loader = jinja2.FileSystemLoader(template_dir)
    # Create template environment
    environment = jinja2.Environment(loader=template_loader)
    # Add `get_lang_from_code` function to the template environment
    # So it can be called in the template
    environment.globals["get_lang_from_code"] = get_lang_from_code
    # Get the report template
    report_template = environment.get_template(name="report_template.html")
    # Render report from template
    # Providing data to be used in the template
    loguru.logger.info("Rendering report from template.")
    report_render = report_template.render(
        username=username,
        friends_bot_likelihood_scores=friends_bot_likelihood_scores,
        datetime_str=datetime_str,
    )
    return report_render


def dump_report(report_render: str, reports_dir: str, username: str) -> str:
    """Dump the rendered friends bot likelihood report to a file.

    Args:
        report_render (str): A unicode formatted string of the rendered report.
        reports_dir (str): The absolute or relative path to the reports directory.
        username (str): The username of the Twitter account the report has been generated for.

    Returns:
        str: The absolute or relative path to the friends bot likelihood report.
    """
    # Create report absolute or relative path
    # Depending on the path provided by the reports_dir parameter
    report_file_path = f"{reports_dir}/@{username}_friends_bot_likelihood_report.html"
    # Dump the report render to a file in the reports directory
    try:
        with open(report_file_path, "w") as report_file:
            report_file.write(report_render)
        loguru.logger.info(f"Report file created at path: {report_file_path}")
        return report_file_path
    except OSError as err:
        loguru.logger.debug(f"Report render dump:\n{report_render}")
        loguru.logger.exception(
            f"Failed to write report render to file at path: {report_file_path}.\n{err}"
        )


# Email function


def send_email_report(
    email_server: str,
    email_server_port: int,
    email_sender_addr: str,
    email_sender_pass: str,
    email_recipient_addr: str,
    report_file_path: str,
    username: str,
) -> None:
    """Send an email with the friends bot likelihood report attached.

    Args:
        email_server (str): The email server to use when sending the email.
        email_server_port (int): The SSL port the email server is listening on.
        email_sender_addr (str): The email address of the sender.
        email_sender_pass (str): The senders email password used to authenticate to the email server.
        email_recipient_addr (str): The recipient email address to send the report to.
        report_file_path (str): The absolute or relative path to the friends bot likelihood report.
        username (str): The username of the Twitter account the report has been generated for.

    Returns:
        None.
    """
    # Set email variables
    email_subject = "Friends Bot Likelihood Report"
    email_body_text = f"Please see the friends bot likelihood report for @{username} attached to this email."
    # Create email multipart message
    message = MIMEMultipart()
    # Add from, to, and email subject to email message
    message["From"] = email_sender_addr
    message["To"] = email_recipient_addr
    message["Subject"] = email_subject
    # Attach email body text to the email multipart message
    message.attach(MIMEText(email_body_text, "plain"))

    # Open the friends bot likelihood report file to be attached to the email
    try:
        with open(report_file_path, "rb") as report_attachment:
            # Create report_part to include the report as an attachment
            # Add report as application/octet-stream
            report_part = MIMEBase("application", "octet-stream")
            # Set the report_part payload to the byte contents of the report
            report_part.set_payload(report_attachment.read())
    except OSError as err:
        loguru.logger.exception(
            f"Failed to open report at path: {report_file_path}.\n{err}"
        )

    # Base64 encode report_part to be attached to the email multipart message
    encoders.encode_base64(report_part)
    # Add headers to the report_part for the report attachment
    report_part.add_header(
        # Get report_file_path basename
        "Content-Disposition",
        "attachment",
        filename=os.path.basename(fr"{report_file_path}"),
    )
    # Add report_part containing the report attachment to the email multipart message
    message.attach(report_part)
    # Convert email multipart message to a string for sending
    message_str = message.as_string()

    # Create secure SSL context for SMTP connection
    # Based on best security practice:
    # https://docs.python.org/3/library/ssl.html#best-defaults
    ssl_context = ssl.create_default_context()

    # Use a context manager to securely connect to the email server
    # Send the email with the report attached
    try:
        loguru.logger.debug(
            f"Connecting to the email server: {email_server} on port: {email_server_port}"
        )
        with smtplib.SMTP_SSL(
            host=email_server, port=email_server_port, context=ssl_context
        ) as smtp_connection:
            # Authenticate with the email server
            loguru.logger.debug(f"Authenticating to the email server: {email_server}")
            smtp_connection.login(user=email_sender_addr, password=email_sender_pass)
            loguru.logger.debug(f"Sending email to: {email_recipient_addr}")
            smtp_connection.sendmail(
                from_addr=email_sender_addr,
                to_addrs=email_recipient_addr,
                msg=message_str,
            )
            loguru.logger.success(
                f"Sent email to: {email_recipient_addr} with the friends bot likelihood report attached."
            )
    # Log any exceptions that can be raised by `login` and `sendmail` methods
    # Terminate the application if one occurs
    except (
        smtplib.SMTPAuthenticationError,
        smtplib.SMTPRecipientsRefused,
        smtplib.SMTPSenderRefused,
        smtplib.SMTPDataError,
    ) as err:
        loguru.logger.exception(
            f"Failed to send email from: {email_sender_addr} to: {email_recipient_addr} using the email server: {email_server}.\n{err}"
        )
