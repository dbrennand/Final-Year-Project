"""Main entrypoint file for the application.

Example usage: python ./src/main.py twitterusername example@email.com
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
    parser.add_argument(
        "email", help="The recipient email address to send the report to."
    )
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
    loguru.logger.info(
        f"Arguments - Username: @{args.username}, Recipient Email Address: {args.email}"
    )
    # Authenticate to the Twitter API (using Tweepy) and Botometer API (using botometer-python)
    twitter_api = twtr.auth(twitter_api_creds=twitter_api_creds)
    botometer_api = botm.auth(botometer_api_creds=botometer_api_creds)
    # Get a list of the Twitter user's friends IDs
    friends_ids = twtr.get_friends_ids(api=twitter_api, username=args.username)
    # Log friends IDs collected for debug purposes
    loguru.logger.debug(f"Collected friends IDs: {friends_ids}")
    # Render friends bot likelihood report from the template
    report_render = helpers.render_report(
        username=args.username,
        friends_bot_likelihood_scores=friends_bot_likelihood_scores,
    )
    # Dump the friends bot likelihood report to a file in the reports directory
    # If the reports directory does not exist, create it
    report_file_path = helpers.dump_report(
        report_render=report_render, username=args.username
    )
    # Finally, send the email with the friends bot likelihood report attached
    helpers.send_email_report(
        email_server=email_creds["EMAIL_SERVER_DOMAIN"],
        email_server_port=int(email_creds["EMAIL_SERVER_PORT"]),
        email_sender_addr=email_creds["EMAIL_SENDER_ADDRESS"],
        email_sender_pass=email_creds["EMAIL_SENDER_PASSWORD"],
        email_recipient_addr=args.email,
        report_file_path=report_file_path,
        username=args.username,
    )
