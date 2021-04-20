"""Unit tests for the modules used in the application.
"""
import pytest
import os
import shutil
import botometer
import tweepy

# Local imports
from modules import botm
from modules import helpers
from modules import twitter as twtr


# See conftest.py for username and email fixtures


@pytest.fixture
def friends_bot_likelihood_scores(username) -> list:
    return [
        {
            "display_scores": {
                "english": {
                    "astroturf": 0.8,
                    "fake_follower": 0.2,
                    "financial": 0.0,
                    "other": 1.4,
                    "overall": 1.6,
                    "self_declared": 0.1,
                    "spammer": 0.5,
                },
                "universal": {
                    "astroturf": 0.6,
                    "fake_follower": 0.4,
                    "financial": 0.0,
                    "other": 1.4,
                    "overall": 1.6,
                    "self_declared": 0.1,
                    "spammer": 0.4,
                },
            },
            "user": {
                "majority_lang": "en",
                "user_data": {
                    "id_str": "123456789",
                    "screen_name": f"{username}",
                },
            },
        },
        {
            "display_scores": {
                "english": {
                    "astroturf": 1.2,
                    "fake_follower": 0.2,
                    "financial": 0.0,
                    "other": 1.3,
                    "overall": 0.4,
                    "self_declared": 0.1,
                    "spammer": 0.1,
                },
                "universal": {
                    "astroturf": 1.2,
                    "fake_follower": 0.2,
                    "financial": 0.0,
                    "other": 1.2,
                    "overall": 0.6,
                    "self_declared": 0.0,
                    "spammer": 0.0,
                },
            },
            "user": {
                "majority_lang": "de",
                "user_data": {"id_str": "123456789", "screen_name": f"{username}"},
            },
        },
    ]


@pytest.fixture
def reports_test_dir(request) -> str:
    # Declare relative path to reports test directory
    # to be created in the relevant tests
    reports_test_dir_path = "./src/test/reports"
    # Add finalizer function to remove reports test directory
    # and its contents once the test has finished
    def remove_reports_dir_contents():
        shutil.rmtree(reports_test_dir_path)

    # Add finalizer function
    request.addfinalizer(remove_reports_dir_contents)
    return reports_test_dir_path


@pytest.fixture
def env_vars() -> list:
    return [
        "TWITTER_API_KEY",
        "TWITTER_API_SECRET",
        "BOTOMETER_API_KEY",
        "EMAIL_SERVER_DOMAIN",
        "EMAIL_SERVER_PORT",
        "EMAIL_SENDER_ADDRESS",
        "EMAIL_SENDER_PASSWORD",
    ]


@pytest.fixture
def botometer_creds() -> dict:
    return helpers.get_env_vars(
        ["TWITTER_API_KEY", "TWITTER_API_SECRET", "BOTOMETER_API_KEY"]
    )


@pytest.fixture
def botometer_auth(botometer_creds) -> botometer.Botometer:
    # Authenticate to the Botometer API
    return botm.auth(
        api_key=botometer_creds["BOTOMETER_API_KEY"],
        consumer_key=botometer_creds["TWITTER_API_KEY"],
        consumer_secret=botometer_creds["TWITTER_API_SECRET"],
    )


@pytest.fixture
def twitter_creds() -> dict:
    return helpers.get_env_vars(
        [
            "TWITTER_API_KEY",
            "TWITTER_API_SECRET",
        ]
    )


@pytest.fixture
def twitter_auth(twitter_creds) -> tweepy.API:
    # Authenticate to the Twitter API
    return twtr.auth(
        consumer_key=twitter_creds["TWITTER_API_KEY"],
        consumer_secret=twitter_creds["TWITTER_API_SECRET"],
    )


@pytest.fixture
def friend_ids() -> list:
    # @elonmusk and @BBCBreaking
    return [44196397, 5402612]


@pytest.fixture
def _get_datetime() -> str:
    # Get current datetime string
    return helpers.get_datetime()


@pytest.mark.utility
def test_get_env_vars_type(env_vars):
    # Get environment variables
    env_vars_dict = helpers.get_env_vars(env_vars)
    # Check env_vars_dict is a dictionary
    assert type(env_vars_dict) == dict


@pytest.mark.utility
def test_get_env_vars(env_vars):
    # Get environment variables
    env_vars_dict = helpers.get_env_vars(env_vars)
    # Get dictionary keys
    env_vars_dict_keys = env_vars_dict.keys()
    # Iterate over environment variables list
    for env_var in env_vars:
        # Check environment variable key is present in the dict
        assert env_var in env_vars_dict_keys


@pytest.mark.utility
def test_get_env_vars_error(caplog):
    # Get environment variables
    env_vars_dict = helpers.get_env_vars(["TEST_ENV_VAR"])
    # Check an error occurred in the logs
    assert (
        "Environment variable: TEST_ENV_VAR is missing. See prerequisite steps in the README file."
        in caplog.text
    )


@pytest.mark.utility
def test_get_datetime(_get_datetime):
    # Check that a string was returned
    # and that "at" is present in the string
    assert (type(datetime_str) == str) and ("at" in datetime_str)


@pytest.mark.parametrize(
    "lang_code, expected_result",
    [
        ("en", "English"),
        ("de", "German"),
        ("fr", "French"),
        # Test "Unknown" is returned when a language code not in
        # ISO 639-1 format is provided
        ("", "Unknown"),
        ("eng", "Unknown"),
        ("This is not a language code", "Unknown"),
    ],
)
@pytest.mark.utility
def test_get_lang_from_code(lang_code, expected_result):
    # Check that the get_lang_from_code function returns the expected result
    assert helpers.get_lang_from_code(lang_code=lang_code) == expected_result


@pytest.mark.utility
def test_create_reports_dir(reports_test_dir):
    # Create reports test directory
    reports_dir = helpers.create_reports_dir(reports_dir=reports_test_dir)
    # Check that the directory has been created
    # and the returned path is the same provided
    assert (os.path.exists(reports_test_dir)) and (reports_dir == reports_test_dir)


@pytest.mark.utility
def test_create_reports_dir_already_exists(reports_test_dir, caplog):
    # Create the reports test directory
    helpers.create_reports_dir(reports_dir=reports_test_dir)
    # Run the function again
    helpers.create_reports_dir(reports_dir=reports_test_dir)
    # Check the logs to verify that the directory creation was skipped as it already existed
    assert (
        f"Reports directory at path: {reports_test_dir} already exists." in caplog.text
    )


@pytest.mark.utility
def test_create_reports_dir_err(caplog):
    invalid_path = "/somedir/that/does/not/exist"
    helpers.create_reports_dir(reports_dir=invalid_path)
    # Verify that an exception occurred in the logs
    assert f"Failed to create reports directory at path: {invalid_path}." in caplog.text


@pytest.mark.botometer
def test_botometer_auth_type(botometer_auth):
    assert isinstance(botometer_auth, botometer.Botometer)


@pytest.mark.botometer
def test_get_friends_bot_likelihood_scores_len_type(botometer_auth, friend_ids):
    friends_bot_likelihood_scores = botm.get_friends_bot_likelihood_scores(
        api=botometer_auth, friends=friend_ids
    )
    # Test returned list length and type
    assert (type(friends_bot_likelihood_scores) == list) and (
        len(friends_bot_likelihood_scores) == 2
    )


@pytest.mark.botometer
def test_get_friends_bot_likelihood_scores_results(botometer_auth, friend_ids):
    friends_bot_likelihood_scores = botm.get_friends_bot_likelihood_scores(
        api=botometer_auth, friends=friend_ids
    )
    for friend_scores in friends_bot_likelihood_scores:
        # Check the data used is present in the Botometer API response
        assert friend_scores["display_scores"]["english"]
        assert friend_scores["display_scores"]["universal"]
        # Check the user ID returned is in the friends_ids list provided
        assert int(friend_scores["user"]["user_data"]["id_str"]) in friend_ids


@pytest.mark.botometer
def test_get_friends_bot_likelihood_scores_err(botometer_auth, caplog):
    # Input a friend ID that does not exist, causing an error
    botm.get_friends_bot_likelihood_scores(api=botometer_auth, friends=[-1])
    # Verify that an exception occurred in the logs
    assert "Failed to get any friends bot likelihood results." in caplog.text


@pytest.mark.twitter
def test_twitter_auth_type(twitter_auth):
    assert isinstance(twitter_auth, tweepy.API)


@pytest.mark.twitter
def test_get_friends_ids_len_types(twitter_auth, username):
    friend_ids_list = twtr.get_friends_ids(api=twitter_auth, username=username)
    # Test returned list length
    # and all items in the list are integers
    assert (type(friend_ids_list) == list) and (
        all(isinstance(friend_id, int) for friend_id in friend_ids_list)
    )


@pytest.mark.twitter
def test_get_friends_ids_err_username(twitter_auth, caplog):
    invalid_username = "This is not a valid username"
    twtr.get_friends_ids(api=twitter_auth, username=invalid_username)
    # Verify that an exception occurred in the logs
    assert f"Failed to get @{invalid_username}'s Twitter friends IDs." in caplog.text


@pytest.mark.twitter
def test_get_friends_ids_err_no_friends(twitter_auth, caplog):
    # A Twitter bot that has no friends
    username = "ProgressYearBar"
    twtr.get_friends_ids(api=twitter_auth, username=username)
    # Verify that an exception occurred in the logs
    assert (
        f"Failed to get any friends IDs for @{username}. It is likely that the account does not have any friends."
        in caplog.text
    )


# Cannot parameterize these tests due to: https://github.com/pytest-dev/pytest/issues/349


@pytest.mark.report
def test_render_report(username, friends_bot_likelihood_scores, _get_datetime):
    assert (
        type(
            helpers.render_report(
                username=username,
                friends_bot_likelihood_scores=friends_bot_likelihood_scores,
                datetime_str=_get_datetime,
            )
        )
        == str
    )


@pytest.mark.report
def test_render_report_no_username(friends_bot_likelihood_scores, _get_datetime):
    assert (
        type(
            helpers.render_report(
                username="",
                friends_bot_likelihood_scores=friends_bot_likelihood_scores,
                datetime_str=_get_datetime,
            )
        )
        == str
    )


@pytest.mark.report
def test_render_report_no_scores(username, _get_datetime):
    assert (
        type(
            helpers.render_report(
                username=username,
                friends_bot_likelihood_scores={},
                datetime_str=_get_datetime,
            )
        )
        == str
    )


@pytest.mark.report
def test_render_report_no_datetime(username, friends_bot_likelihood_scores):
    assert (
        type(
            helpers.render_report(
                username=username,
                friends_bot_likelihood_scores=friends_bot_likelihood_scores,
                datetime_str="",
            )
        )
        == str
    )


@pytest.mark.report
def test_dump_report(
    reports_test_dir, username, friends_bot_likelihood_scores, _get_datetime
):
    # Create reports test directory
    reports_dir = helpers.create_reports_dir(reports_dir=reports_test_dir)
    # Render the friends bot likelihood report from the template
    report_render = helpers.render_report(
        username=username,
        friends_bot_likelihood_scores=friends_bot_likelihood_scores,
        datetime_str=_get_datetime,
    )
    # Dump report render to a file in the reports directory
    report_file_path = helpers.dump_report(
        report_render=report_render, reports_dir=reports_dir, username=username
    )
    # Check the report render was dumped to a file
    assert os.path.exists(report_file_path)


@pytest.mark.email
def test_send_email_report(
    env_vars,
    reports_test_dir,
    friends_bot_likelihood_scores,
    _get_datetime,
    email,
    username,
    caplog,
):
    creds = helpers.get_env_vars(env_vars)
    # Create reports test directory
    reports_dir = helpers.create_reports_dir(reports_dir=reports_test_dir)
    # Render the friends bot likelihood report from the template
    report_render = helpers.render_report(
        username=username,
        friends_bot_likelihood_scores=friends_bot_likelihood_scores,
        datetime_str=_get_datetime,
    )
    # Dump report render to a file in the reports directory
    report_file_path = helpers.dump_report(
        report_render=report_render, reports_dir=reports_dir, username=username
    )
    # Send email with report attached
    helpers.send_email_report(
        email_server=creds["EMAIL_SERVER_DOMAIN"],
        email_server_port=int(creds["EMAIL_SERVER_PORT"]),
        email_sender_addr=creds["EMAIL_SENDER_ADDRESS"],
        email_sender_pass=creds["EMAIL_SENDER_PASSWORD"],
        email_recipient_addr=email,
        report_file_path=report_file_path,
        username=username,
    )
    assert (
        f"Sent email to: {email} with the friends bot likelihood report attached."
        in caplog.text
    )
