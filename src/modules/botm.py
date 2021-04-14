"""Module containing Botometer functions for the application.
"""
import botometer
import loguru


def auth(botometer_api_creds: dict) -> botometer.Botometer:
    """Authenticate to the Botometer API using botometer-python.

    NOTE: botometer-python also authenticates to the Twitter API.

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


def get_friends_bot_likelihood_scores(api: botometer.Botometer, friends: list) -> list:
    """Get bot likelihood scores for Twitter friends.

    https://github.com/IUNetSci/botometer-python/blob/master/botometer/__init__.py#L140

    Args:
        api (botometer.Botometer): A botometer.Botometer object authenticated to the Botometer and Twitter API.
        friends (list): A list containing a Twitter account's friends (represented as IDs).

    Returns:
        list: A list containing the bot likelihood scores for each Twitter friend.
    """
    loguru.logger.info("Getting Twitter friends bot likelihood scores from Botometer.")
    # Initialise list containing each friend's bot likelihood score
    # List contains dictionaries with the bot likelihood scores for each friend
    friends_bot_likelihood_scores = []
    try:
        # Get all friends bot likelihood scores from the Botometer API
        # Retry 3 times for each friend if an exception occurs
        for friend_id, results in api.check_accounts_in(
            accounts=friends, full_user_object=False, retries=3
        ):
            # A TweepyError or NoTimelineError can occur when Botometer checks a friend
            # https://github.com/IUNetSci/botometer-python/blob/master/botometer/__init__.py#L153
            # When these occur the result is a dictionary containing an error message:
            # {"error": err_msg}
            # Check first if this type of result has been returned
            error_msg = results.get("error", None)
            if error_msg:
                # Error message has been returned as the result
                # Log a warning message
                loguru.logger.warning(
                    f"Botometer returned the following error for friend: {friend_id}.\n{error_msg}"
                )
            # Got a successful response for this friend from the Botometer API
            else:
                # Example JSON response: https://github.com/IUNetSci/botometer-python#botometer-v4
                # Get friend's Twitter username (screen name)
                friend_username = results["user"]["user_data"]["screen_name"]
                loguru.logger.success(
                    f"Got bot likelihood results from Botometer for friend: @{friend_username}, {friend_id}."
                )
                # Add friend's bot likelihood results to the list
                loguru.logger.debug(
                    "Adding bot likelihood results for friend: {friend_username}, {friend_id} to the list."
                )
                friends_bot_likelihood_scores.append(results)
        loguru.logger.info("All friends bot likelihood scores have been collected.")
        return friends_bot_likelihood_scores
    # The `check_accounts_in` method can raise the following exceptions once all retires have been exhausted:
    # requests: ConnectionError, HTTPError, Timeout
    ## https://github.com/IUNetSci/botometer-python/blob/master/botometer/__init__.py#L159
    # Standard Python Exception
    ## https://github.com/IUNetSci/botometer-python/blob/master/botometer/__init__.py#L164
    # If one of these occur, the application should return the friend bot likelihood scores it has collected
    # up to the point of failure. As long as it has not failed on the first attempt (as the list would be empty)
    except (
        botometer.ConnectionError,
        botometer.HTTPError,
        botometer.Timeout,
        Exception,
    ) as err:
        loguru.logger.warning(
            f"An exception occurred: {err} and all retries to Botometer have been exhausted."
        )
        loguru.logger.debug(
            "Checking if the friends bot likelihood scores list has at least one result."
        )
        if len(friends_bot_likelihood_scores) >= 1:
            loguru.logger.debug(
                "Friends bot likelihood scores list has at least one result."
            )
            return friends_bot_likelihood_scores
        else:
            # The list contains no results, log a terminating error
            loguru.logger.exception(
                f"No friends bot likelihood results were collected.\n{err}"
            )
