"""Main entrypoint file for the application.

Example usage: python ./src/main.py twitterusername example@email.com --save /path/to/save/report/on/disk
"""
import argparse

# Local imports
import modules.helpers as helpers
import modules.botometer as botm
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
    helpers.init_logger()
    # Parse CLI arguments
    args = parse_args()
    # Log username and email arguments
    helpers.log_message(f"Username: {args.username} Email: {args.email}.")
