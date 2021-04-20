"""Module containing Twitter functions for the application.
"""
import tweepy
import loguru

# Local import
import modules.helpers as helpers


def auth(consumer_key: str, consumer_secret: str) -> tweepy.API:
    """Authenticate to the Twitter API using Tweepy.

    https://docs.tweepy.org/en/latest/api.html#tweepy.API

    Args:
        consumer_key (str): A string containing the Twitter API consumer key.
        consumer_secret (str): A string containing the Twitter API consumer secret.

    Returns:
        tweepy.API: A Tweepy.API object authenticated to the Twitter API.
    """
    loguru.logger.info("Authenticating to the Twitter API.")
    # Initialise Tweepy application authentication flow
    auth = tweepy.AppAuthHandler(
        consumer_key=consumer_key, consumer_secret=consumer_secret
    )
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
        Using `api.friends_ids` method over `api.friends` because it provides greater API results before hitting the rate limit.
            See: https://github.com/tweepy/tweepy/issues/1431
    """
    loguru.logger.info(f"Getting @{username}'s Twitter friends IDs.")
    # Initialise friends IDs list
    friends_ids_list = []
    # The Twitter API returns results in pages
    # Use Tweepy's Cursor class to interate over all friends IDs on every page
    # Get the maximum number of friends IDs in a single request (5000)
    try:
        for friend_id in tweepy.Cursor(
            api.friends_ids, screen_name=username, count=5000
        ).items():
            loguru.logger.debug(f"Found friend with ID: {friend_id}")
            friends_ids_list.append(friend_id)
    except tweepy.TweepError as err:
        loguru.logger.exception(
            f"Failed to get @{username}'s Twitter friends IDs.\n{err}"
        )
    # Check if the list has one or more results
    if helpers.check_list_populated(_list=friends_ids_list):
        # The list contains at least one or more results
        loguru.logger.debug("One or more friends IDs were found.")
        return friends_ids_list
    else:
        # The list contains no results, log a terminating error
        loguru.logger.exception(
            f"Failed to get any friends IDs for @{username}. It is likely that their account does not have any friends."
        )
