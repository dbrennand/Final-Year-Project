"""Main entrypoint file for the application.

Example usage: python ./src/main.py twitterusername example@email.com --save /path/to/save/report/on/disk
"""
import argparse
import loguru

# Local imports
import modules.helpers as helpers
import modules.botm as botm
import modules.twitter as twtr


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments.

    Returns:
        argparse.Namespace: A Namespace object containing string representations of the input arguments.
    """
    # Create argument parser for application
    parser = argparse.ArgumentParser(
        description="Generates and emails a report containing bot likelihood scores for a Twitter user's friends."
    )
    # Add arguments to parser
    parser.add_argument("username", help="The Twitter username to obtain friends for.")
    parser.add_argument("email", help="The email address to send the report to.")
    # Parse arguments and return
    return parser.parse_args()


if __name__ == "__main__":
    # Initialise logging
    helpers.init_log_handler()
    # Get API and email credentials
    twitter_api_creds, botometer_api_creds = helpers.get_api_creds()
    email_creds = helpers.get_email_creds()
    # Parse CLI arguments
    args = parse_args()
    # Log username and email arguments
    loguru.logger.info("Username: @{args.username} Email: {args.email}")
    # Authenticate to the Twitter API (using Tweepy) and Botometer API (using botometer-python)
    twitter_api = twtr.auth(twitter_api_creds=twitter_api_creds)
    botometer_api = botm.auth(botometer_api_creds=botometer_api_creds)
