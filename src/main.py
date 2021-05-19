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
    parser.add_argument(
        "username", type=str, help="The Twitter username to obtain friends for."
    )
    parser.add_argument(
        "email", type=str, help="The recipient email address to send the report to."
    )
    # Add argument for demo mode
    parser.add_argument(
        "-d",
        "--demo",
        default=False,
        action="store_true",
        help="Flag to run the application in demo mode.",
    )
    # Parse arguments and return
    return parser.parse_args()


if __name__ == "__main__":
    # Initialise logging
    helpers.init_log_handler()
    # Parse CLI arguments
    args = parse_args()
    # Log username, email and demo arguments
    loguru.logger.info(
        f"Arguments - Username: @{args.username}, Recipient Email Address: {args.email}, Demo Mode: {args.demo}"
    )
    # Check if the demo argument has been provided
    # to run the application in demo mode
    if args.demo:
        # Get email credentials
        creds = helpers.get_env_vars(
            [
                "EMAIL_SERVER_DOMAIN",
                "EMAIL_SERVER_PORT",
                "EMAIL_SENDER_ADDRESS",
                "EMAIL_SENDER_PASSWORD",
            ]
        )
        loguru.logger.info("Demo argument provided, running application in demo mode.")
        # Get generated friends bot likelihood scores for the demo
        friends_bot_likelihood_scores = helpers.get_demo_friends_bot_likelihood_scores()
    else:
        # Demo argument has not been provided
        # Get API and email credentials
        creds = helpers.get_env_vars(
            [
                "TWITTER_API_KEY",
                "TWITTER_API_SECRET",
                "BOTOMETER_API_KEY",
                "EMAIL_SERVER_DOMAIN",
                "EMAIL_SERVER_PORT",
                "EMAIL_SENDER_ADDRESS",
                "EMAIL_SENDER_PASSWORD",
            ]
        )
        # Authenticate to the Twitter API (using Tweepy) and Botometer API (using botometer-python)
        twitter_api = twtr.auth(
            consumer_key=creds["TWITTER_API_KEY"],
            consumer_secret=creds["TWITTER_API_SECRET"],
        )
        botometer_api = botm.auth(
            api_key=creds["BOTOMETER_API_KEY"],
            consumer_key=creds["TWITTER_API_KEY"],
            consumer_secret=creds["TWITTER_API_SECRET"],
        )
        # Get a list of the Twitter user's friends IDs
        friends_ids = twtr.get_friends_ids(api=twitter_api, username=args.username)
        # Log friends IDs collected for debug purposes
        loguru.logger.debug(f"Collected friends IDs: {friends_ids}")
        # Get a list of the Twitter user's friends bot likelihood scores
        friends_bot_likelihood_scores = botm.get_friends_bot_likelihood_scores(
            api=botometer_api, friends=friends_ids
        )
    # Run below regardless of whether demo argument has or has not been provided
    # Get current datetime string to be used for the report render
    datetime_str = helpers.get_datetime()
    # Render friends bot likelihood report from the template
    report_render = helpers.render_report(
        username=args.username,
        friends_bot_likelihood_scores=friends_bot_likelihood_scores,
        datetime_str=datetime_str,
    )
    # Create reports directory to dump the friends bot likelihood report to
    reports_dir = helpers.create_reports_dir()
    # Dump the friends bot likelihood report to a file in the reports directory
    report_file_path = helpers.dump_report(
        report_render=report_render,
        reports_dir=reports_dir,
        username=args.username,
    )
    # Finally, send the email with the friends bot likelihood report attached
    helpers.send_email_report(
        email_server=creds["EMAIL_SERVER_DOMAIN"],
        email_server_port=int(creds["EMAIL_SERVER_PORT"]),
        email_sender_addr=creds["EMAIL_SENDER_ADDRESS"],
        email_sender_pass=creds["EMAIL_SENDER_PASSWORD"],
        email_recipient_addr=args.email,
        report_file_path=report_file_path,
        username=args.username,
    )
