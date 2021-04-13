"""Module containing Twitter functions for the application.
"""
import tweepy

# Local import
import modules.helpers as helpers


def auth(twitter_api_creds: dict) -> tweepy.API:
    """Authenticate to the Twitter API using Tweepy.

    https://docs.tweepy.org/en/latest/api.html#tweepy.API

    Args:
        twitter_api_creds (dict): A dictionary containing the Twitter application API credentials.
            Credentials are the API key and secret (also known as consumer key and secret respectively).

    Returns:
        tweepy.API: A Tweepy.API object authenticated to the Twitter API.
    """
    # Initialise Tweepy application authentication flow
    auth = tweepy.AppAuthHandler(**twitter_api_creds)
    # Create and return an authenticated Tweepy API object
    # Retry 2 times if a request fails with a 3 second delay between retries
    # Wait if the application hits the Twitter API rate limit
    return tweepy.API(auth, retry_count=2, retry_delay=3, wait_on_rate_limit=True)


def get_friends_ids(api: tweepy.API, username: str) -> list:
    """Get a Twitter user's friends IDs.

    https://docs.tweepy.org/en/latest/api.html#tweepy.API.friends_ids

    https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-friends-ids

    Args:
        api (tweepy.API): A Tweepy API object authenticated to the Twitter API.
        username (str): The username of the Twitter account to collect friends IDs for.

    Returns:
        list: A list containing all of the specified user's friends. Represented as IDs.

    Notes:
        Using `api.friends_ids` method over `api.friends` because it provides 5000 results per 15 minute rate limit (5000/15mins) window vs the latter's 200/15mins.
    """
    # Initialise friends IDs list
    friends_ids_list = []
    # The Twitter API returns results in pages
    # Use Tweepy's Cursor class to interate over all friends IDs on every page
    try:
        for friend_id in tweepy.Cursor(api.friends_ids, screen_name=username).items():
            friends_ids_list.append(friend_id)
    except tweepy.TweepError as err:
        helpers.log_message(
            message=f"An error occurred retrieving {username}'s Twitter friends.\n{err}",
            level="ERROR",
        )
    return friends_ids_list
