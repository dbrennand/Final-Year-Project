"""Module containing Twitter functions for the application.
"""
import tweepy

# Local import
import modules.helpers as helpers


def auth(twitter_creds: dict) -> tweepy.API:
    """Authenticate to the Twitter API using Tweepy.

    https://docs.tweepy.org/en/latest/api.html#tweepy.API

    Args:
        twitter_creds (dict): A dictionary containing the Twitter application API credentials.
            Credentials are the API key and secret (also known as consumer key and secret respectively).

    Returns:
        tweepy.API: A Tweepy API object authenticated to the Twitter API.
    """
    # Initialise Tweepy application authentication flow
    auth = tweepy.AppAuthHandler(**twitter_creds)
    # Create and return an authenticated Tweepy API object
    # Retry 2 times if a request fails with a 3 second delay between retries
    # Wait if the application hits the Twitter API rate limit
    return tweepy.API(auth, retry_count=2, retry_delay=3, wait_on_rate_limit=True)
