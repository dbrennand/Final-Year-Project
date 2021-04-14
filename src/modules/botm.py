"""Module containing Botometer functions for the application.
"""
import botometer
import loguru


def auth(botometer_api_creds: dict) -> botometer.Botometer:
    """Authenticate to the Botometer API using botometer-python.

    Args:
        botometer_api_creds (dict): A dictionary containing the required credentials for the Botometer constructor
            to authenticate to the Botometer and Twitter API.

    Returns:
        botometer.Botometer: A botometer.Botometer object authenticated to the Botometer and Twitter API.
    """
    loguru.logger.info("Authenticating to the Botometer API.")
    # Initialise botometer constructor and provide API credentials
    # Provide the same Tweepy parameters to the constructor
    return botometer.Botometer(
        **botometer_api_creds,
        tweepy_kwargs={"retry_count": 2, "retry_delay": 3},
        wait_on_ratelimit=True,
    )


# TODO: Function to get Twitter friend bot likelihood score
