"""Unit tests for the modules used in the application.
"""
import pytest
import pytest_mock
import os
import shutil
import botometer
import tweepy
import datetime

# Local imports
from modules import botm
from modules import helpers
from modules import twitter as twtr


# See conftest.py for username and email fixtures


@pytest.fixture
def friends_bot_likelihood_scores(username: str) -> list:
    """Returns an example JSON response from the Botometer API.

    Args:
        username (str): A username provided by the pytest username fixture.

    Returns:
        list: A list containing the bot likelihood scores for each Twitter friend.
    """
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
def reports_test_dir(request: pytest.FixtureRequest) -> str:
    """Returns the relative path to the test reports directory.

    Also, adds a finaliser function to remove the test reports directory and its contents
    once the test has completed.

    Args:
        request (pytest.FixtureRequest): A pytest fixture providing information of the requesting test function.

    Returns:
        str: The relative path to the test reports directory.
    """
    # Declare relative path to the test reports directory
    # to be created in the relevant tests
    reports_test_dir_path = "./src/test/reports"
    # Add finalizer function to remove the test reports directory
    # and its contents once the test has finished
    def remove_reports_dir_contents():
        shutil.rmtree(reports_test_dir_path)

    # Add finalizer function
    request.addfinalizer(remove_reports_dir_contents)
    return reports_test_dir_path


@pytest.fixture
def botometer_creds() -> dict:
    """Helper fixture to return Botometer API credentials in multiple tests.

    See helpers.get_env_vars() for further details.

    Returns:
        dict: A dictionary containing the Botometer and Twitter API credentials.
    """
    # Get environment variables to authenticate to the Botometer API
    return helpers.get_env_vars(
        ["TWITTER_API_KEY", "TWITTER_API_SECRET", "BOTOMETER_API_KEY"]
    )


@pytest.fixture
def botometer_auth(botometer_creds: dict) -> botometer.Botometer:
    """Helper fixture to return an authenticated botometer.Botometer object in multiple tests.

    Args:
        botometer_creds (dict): A dictionary containing the Botometer and Twitter API credentials.

    Returns:
        botometer.Botometer: A botometer.Botometer object authenticated to the Botometer and Twitter API.
    """
    return botm.auth(
        api_key=botometer_creds["BOTOMETER_API_KEY"],
        consumer_key=botometer_creds["TWITTER_API_KEY"],
        consumer_secret=botometer_creds["TWITTER_API_SECRET"],
    )


@pytest.fixture
def twitter_creds() -> dict:
    """Helper fixture to return Twitter API credentials in multiple tests.

    See helpers.get_env_vars() for further details.

    Returns:
        dict: A dictionary containing the Twitter API credentials.
    """
    return helpers.get_env_vars(
        [
            "TWITTER_API_KEY",
            "TWITTER_API_SECRET",
        ]
    )


@pytest.fixture
def twitter_auth(twitter_creds: dict) -> tweepy.API:
    """Helper fixture to return an authenticated tweepy.API object in multiple tests.

    Args:
        twitter_creds (dict): A dictionary containing the Twitter API credentials.

    Returns:
        tweepy.API: A Tweepy.API object authenticated to the Twitter API.
    """
    # Authenticate to the Twitter API
    return twtr.auth(
        consumer_key=twitter_creds["TWITTER_API_KEY"],
        consumer_secret=twitter_creds["TWITTER_API_SECRET"],
    )


@pytest.fixture
def friend_ids() -> list:
    """Helper fixture to return a list of Twitter friend IDs in multiple tests.

    Returns:
        list: A list containing two Twitter friend IDs.
    """
    # @elonmusk and @BBCBreaking
    return [44196397, 5402612]


@pytest.fixture
def _get_datetime() -> str:
    """Helper fixture to return the current datetime string.

    See helpers.get_datetime() for further details.

    Returns:
        str: A string representing the current datetime.
            Example return format: "23/04/2021 at 12:00:01".
    """
    # Get current datetime string
    return helpers.get_datetime()


class TestGetEnvVars:
    """A class containing multiple tests for helpers.get_env_vars()."""

    # Declare environment variable names to get in the tests
    env_var_names = ["TWITTER_API_KEY", "TWITTER_API_SECRET", "BOTOMETER_API_KEY"]

    @pytest.fixture(autouse=True)
    def mock_os_environ(self, mocker: pytest_mock.MockerFixture) -> None:
        """Mocker fixture to run for every test inside the class.

        Args:
            mocker (pytest_mock.MockerFixture): A pytest_mock.MockerFixture providing a
                thin-wrapper around the patching API from the mock library.
        """
        # Patch os.environ to return pre-set environment variables
        mocker.patch.dict(
            "os.environ",
            dict(
                TWITTER_API_KEY="API key",
                TWITTER_API_SECRET="API secret",
                BOTOMETER_API_KEY="API key",
            ),
        )

    @pytest.mark.utility
    def test_get_env_vars_type(self) -> None:
        """Test the return value type from helpers.get_env_vars()."""
        # Get environment variables
        env_vars_dict = helpers.get_env_vars(self.env_var_names)
        # Check env_vars_dict is a dictionary
        assert type(env_vars_dict) == dict

    @pytest.mark.utility
    def test_get_env_vars(self) -> None:
        """Test the expected dictionary keys and values are returned from helpers.get_env_vars()."""
        # Get environment variables
        env_vars = helpers.get_env_vars(self.env_var_names)
        # Check env_vars contains the mocked dict key value pairs
        assert env_vars == dict(
            TWITTER_API_KEY="API key",
            TWITTER_API_SECRET="API secret",
            BOTOMETER_API_KEY="API key",
        )

    @pytest.mark.utility
    def test_get_env_vars_error(self, caplog) -> None:
        """Test an error occurs in the logs for a non-existent environment variable.

        Args:
            caplog: A pytest caplog fixture used to examine application log messages.
        """
        # Get an environment variable that is not present
        env_vars_dict = helpers.get_env_vars(["TEST_ENV_VAR"])
        # Check an error occurred in the logs
        assert (
            "Environment variable: TEST_ENV_VAR is missing. See prerequisite steps in the README file."
            in caplog.text
        )


@pytest.mark.utility
def test_get_datetime(mocker: pytest_mock.MockerFixture) -> None:
    """Test helpers.get_datetime() returns the mocked value in the expected format.

    Args:
        mocker (pytest_mock.MockerFixture): A pytest_mock.MockerFixture providing a
            thin-wrapper around the patching API from the mock library.
    """
    # Mock datetime to test helpers.get_datetime function
    mock_dt = mocker.patch("modules.helpers.datetime")
    # Alter return value of datetime.now() to a specific date to test against
    mock_dt.datetime.now.return_value = datetime.datetime(2021, 4, 23, 12, 0, 1)
    # Get datetime string
    dt = helpers.get_datetime()
    # Check that a string was returned and is the mocked value
    assert "23/04/2021 at 12:00:01" == dt


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
def test_get_lang_from_code(lang_code: str, expected_result: str) -> None:
    """Test helpers.get_lang_from_code() returns the expected value
        given a string for the parameter lang_code.

    Args:
        lang_code (str): A string for the test to be provided to the lang_code parameter.
        expected_result (str): The expected return value from helpers.get_lang_from_code().
    """
    # Check that helpers.get_lang_from_code() function returns the expected result
    # for each parameterised test
    assert helpers.get_lang_from_code(lang_code=lang_code) == expected_result


@pytest.mark.utility
def test_create_reports_dir(reports_test_dir: str) -> None:
    """Test helpers.create_reports_dir() creates the test reports directory.

    Args:
        reports_test_dir (str): The relative path to the test reports directory.
    """
    # Create test reports directory
    reports_dir = helpers.create_reports_dir(reports_dir=reports_test_dir)
    # Check that the directory has been created
    # and the returned path is the same provided
    assert (os.path.exists(reports_test_dir)) and (reports_dir == reports_test_dir)


@pytest.mark.utility
def test_create_reports_dir_already_exists(reports_test_dir: str, caplog) -> None:
    """Test helpers.create_reports_dir() skips creating the test reports directory
        if it already exists.

    Args:
        reports_test_dir (str): The relative path to the test reports directory.
        caplog: A pytest caplog fixture used to examine application log messages.
    """
    # Create the test reports directory
    helpers.create_reports_dir(reports_dir=reports_test_dir)
    # Run the function again
    helpers.create_reports_dir(reports_dir=reports_test_dir)
    # Check the logs to verify that the directory creation was skipped as it already existed
    assert (
        f"Reports directory at path: {reports_test_dir} already exists." in caplog.text
    )


@pytest.mark.utility
def test_create_reports_dir_err(caplog) -> None:
    """Test helpers.create_reports_dir() logs an error message when an invalid path is provided.

    Args:
        caplog: A pytest caplog fixture used to examine application log messages.
    """
    invalid_path = "/somedir/that/does/not/exist"
    helpers.create_reports_dir(reports_dir=invalid_path)
    # Verify that an exception occurred in the logs
    assert f"Failed to create reports directory at path: {invalid_path}." in caplog.text


@pytest.mark.utility
@pytest.mark.demo
def test_get_username_type(faker) -> None:
    """Test helpers.get_username() returns a string.

    Args:
        faker: A faker fixture for pytest.
    """
    assert type(helpers.get_username(api=faker)) == str


@pytest.mark.utility
@pytest.mark.demo
# https://faker.readthedocs.io/en/master/pytest-fixtures.html
def test_get_username(mocker: pytest_mock.MockerFixture, faker) -> None:
    """Test helpers.get_username() returns the expected usernames when seeded.

    Args:
        mocker (pytest_mock.MockerFixture): A pytest_mock.MockerFixture providing a
            thin-wrapper around the patching API from the mock library.
        faker: A faker fixture for pytest.
    """
    expected_usernames = ["zoconnor", "melissa34", "hmartin", "ogreen", "cheryllopez"]
    # Seed faker for this test
    faker.seed_instance(12345)
    # Create spy for helpers.get_username()
    spy_get_username = mocker.spy(helpers, "get_username")
    # Get 5 usernames and check they are expected from the seed value
    for num in range(5):
        # Get a username
        username = helpers.get_username(api=faker)
        # Check its the expected username
        assert username == expected_usernames[num]
    # Check that helpers.get_username() was called 5 times
    assert spy_get_username.call_count == 5


@pytest.mark.utility
@pytest.mark.demo
def test_get_scores_len_type(faker) -> None:
    """Test helpers.get_scores() returns a list of the expected length
    and all items in the list are integers.

    Args:
        faker: A faker fixture for pytest.
    """
    # Get 7 random scores
    scores = helpers.get_scores(api=faker)
    # Test returned type, length and all items in the list are integers
    assert (
        (type(scores) == list)
        and (all(isinstance(score, float) for score in scores))
        and (len(scores) == 7)
    )


@pytest.mark.utility
@pytest.mark.demo
def test_get_scores(faker) -> None:
    """Test helpers.get_scores() returns the expected scores when seeded.

    Args:
        faker: A faker fixture for pytest.
    """
    expected_scores = [3.8, 1.2, 3.9, 2.2, 1.1, 3.8, 3.9]
    # Seed faker for this test
    faker.seed_instance(2468)
    # Get 7 scores and check they are expected from the seed value
    scores = helpers.get_scores(api=faker)
    for score in scores:
        assert score in expected_scores


@pytest.mark.utility
@pytest.mark.demo
def test_get_demo_friends_bot_likelihood_scores_len_type() -> None:
    """Test helpers.get_demo_friends_bot_likelihood_scores() returns a list of the
    expected length.
    """
    gen_friends_bot_likelihood_scores = helpers.get_demo_friends_bot_likelihood_scores()
    # Test returned list length and type
    assert (type(gen_friends_bot_likelihood_scores) == list) and (
        len(gen_friends_bot_likelihood_scores) == 15
    )


@pytest.mark.botometer
def test_botometer_auth(mocker: pytest_mock.MockerFixture) -> None:
    """Test botm.auth() is invoked with the correct parameters.

    Args:
        mocker (pytest_mock.MockerFixture): A pytest_mock.MockerFixture providing a
            thin-wrapper around the patching API from the mock library.
    """
    mock_botm = mocker.patch("modules.botm.botometer")
    # Create a mock version of botometer.Botometer
    auth = botm.auth(
        api_key="API key", consumer_key="API key", consumer_secret="API secret"
    )
    # Validate that the mock version of botometer.Botometer was invoked with the correct
    # parameters
    mock_botm.Botometer.assert_called_with(
        rapidapi_key="API key",
        consumer_key="API key",
        consumer_secret="API secret",
        tweepy_kwargs={"retry_count": 2, "retry_delay": 3},
        wait_on_ratelimit=True,
    )


@pytest.mark.botometer
def test_botometer_auth_type(botometer_auth: botometer.Botometer) -> None:
    """Test botm.auth() (invoked in the botometer_auth fixture)
        returns an instance of botometer.Botometer.

    Args:
        botometer_auth (botometer.Botometer): A botometer.Botometer object authenticated to the Botometer and Twitter API.
    """
    assert isinstance(botometer_auth, botometer.Botometer)


@pytest.mark.botometer
def test_get_friends_bot_likelihood_scores_len_type(
    botometer_auth: botometer.Botometer, friend_ids: list
) -> None:
    """Test botm.get_friends_bot_likelihood_scores() returns a list of the expected length.

    Args:
        botometer_auth (botometer.Botometer): A botometer.Botometer object authenticated to the Botometer and Twitter API.
        friend_ids (list): A list containing two Twitter friend IDs.
    """
    friends_bot_likelihood_scores = botm.get_friends_bot_likelihood_scores(
        api=botometer_auth, friends=friend_ids
    )
    # Test returned list length and type
    assert (type(friends_bot_likelihood_scores) == list) and (
        len(friends_bot_likelihood_scores) == 2
    )


@pytest.mark.botometer
def test_get_friends_bot_likelihood_scores_results(
    botometer_auth: botometer.Botometer, friend_ids: list
) -> None:
    """Test botm.get_friends_bot_likelihood_scores() returns the expected
        JSON results from the Botometer API for each friend ID provided.

    Args:
        botometer_auth (botometer.Botometer): A botometer.Botometer object authenticated to the Botometer and Twitter API.
        friend_ids (list): A list containing two Twitter friend IDs.
    """
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
def test_get_friends_bot_likelihood_scores_err(
    botometer_auth: botometer.Botometer, caplog
) -> None:
    """Test botm.get_friends_bot_likelihood_scores() logs an error when
        provided an invalid friend ID.

    Args:
        botometer_auth (botometer.Botometer): A botometer.Botometer object authenticated to the Botometer and Twitter API.
        caplog: A pytest caplog fixture used to examine application log messages.
    """
    # Input a friend ID that does not exist, causing an error to be logged
    botm.get_friends_bot_likelihood_scores(api=botometer_auth, friends=[-1])
    # Verify that an exception occurred in the logs
    assert "Failed to get any friends bot likelihood results." in caplog.text


@pytest.mark.twitter
def test_twitter_auth_type(twitter_auth: tweepy.API) -> None:
    """Test twtr.auth() (invoked in the twitter_auth fixture)
        returns an instance of tweepy.API.

    Args:
        twitter_auth (tweepy.API): A Tweepy.API object authenticated to the Twitter API.
    """
    assert isinstance(twitter_auth, tweepy.API)


@pytest.mark.twitter
def test_get_friends_ids_len_types(twitter_auth: tweepy.API, username: str) -> None:
    """Test twtr.get_friends_ids() returns a list of the expected length and that all values
        in the list are integers.

    Args:
        twitter_auth (tweepy.API): A Tweepy.API object authenticated to the Twitter API.
        username (str): A username provided by the pytest username fixture.
    """
    friend_ids_list = twtr.get_friends_ids(api=twitter_auth, username=username)
    # Test returned list length
    # and all items in the list are integers
    assert (type(friend_ids_list) == list) and (
        all(isinstance(friend_id, int) for friend_id in friend_ids_list)
    )


@pytest.mark.twitter
def test_get_friends_ids_err_username(twitter_auth: tweepy.API, caplog) -> None:
    """Test twtr.get_friends_ids() logs an error when provided an invalid username to get Twitter
        friend IDs for.

    Args:
        twitter_auth (tweepy.API): A Tweepy.API object authenticated to the Twitter API.
        caplog: A pytest caplog fixture used to examine application log messages.
    """
    # Declare an invalid username
    invalid_username = "This is not a valid username"
    twtr.get_friends_ids(api=twitter_auth, username=invalid_username)
    # Verify that an exception occurred in the logs
    assert f"Failed to get @{invalid_username}'s Twitter friends IDs." in caplog.text


@pytest.mark.twitter
def test_get_friends_ids_err_no_friends(twitter_auth: tweepy.API, caplog) -> None:
    """Test twtr.get_friends_ids() logs an error when provided a Twitter user that is not following anyone (has no friends).

    Args:
        twitter_auth (tweepy.API): A Tweepy.API object authenticated to the Twitter API.
        caplog: A pytest caplog fixture used to examine application log messages.
    """
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
def test_render_report(
    username: str, friends_bot_likelihood_scores: list, _get_datetime: str
) -> None:
    """Test helpers.render_report() returns a string when provided all parameters.

    Args:
        username (str): A username provided by the pytest username fixture.
        friends_bot_likelihood_scores (list): A list containing the bot likelihood scores for each Twitter friend.
        _get_datetime (str): A string representing the current datetime.
    """
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
def test_render_report_no_username(
    friends_bot_likelihood_scores: list, _get_datetime: str
) -> None:
    """Test helpers.render_report() returns a string when the username parameter is empty string.

    Args:
        friends_bot_likelihood_scores (list): A list containing the bot likelihood scores for each Twitter friend.
        _get_datetime (str): A string representing the current datetime.
    """
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
def test_render_report_no_scores(username: str, _get_datetime: str) -> None:
    """Test helpers.render_report() returns a string when the
        friends_bot_likelihood_scores parameter is an empty dictionary.

    Args:
        username (str): A username provided by the pytest username fixture.
        _get_datetime (str): A string representing the current datetime.
    """
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
def test_render_report_no_datetime(
    username: str, friends_bot_likelihood_scores: list
) -> None:
    """Test helpers.render_report() returns a string when the datetime_str parameter is an empty string.

    Args:
        username (str): A username provided by the pytest username fixture.
        friends_bot_likelihood_scores (list): A list containing the bot likelihood scores for each Twitter friend.
    """
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
    reports_test_dir: str,
    username: str,
    friends_bot_likelihood_scores: list,
    _get_datetime: str,
) -> None:
    """Test helpers.dump_report() creates a report file at the returned file path.

    Args:
        reports_test_dir (str): The relative path to the test reports directory.
        username (str): A username provided by the pytest username fixture.
        friends_bot_likelihood_scores (list): A list containing the bot likelihood scores for each Twitter friend.
        _get_datetime (str): A string representing the current datetime.
    """
    # Create test reports directory
    reports_dir = helpers.create_reports_dir(reports_dir=reports_test_dir)
    # Render the friends bot likelihood report from the template
    report_render = helpers.render_report(
        username=username,
        friends_bot_likelihood_scores=friends_bot_likelihood_scores,
        datetime_str=_get_datetime,
    )
    # Dump report render to a file in the test reports directory
    report_file_path = helpers.dump_report(
        report_render=report_render, reports_dir=reports_dir, username=username
    )
    # Check the report was dumped at the file path returned
    assert os.path.exists(report_file_path)


@pytest.mark.email
def test_send_email_report(
    reports_test_dir: str,
    friends_bot_likelihood_scores: list,
    _get_datetime: str,
    email: str,
    username: str,
    caplog,
) -> None:
    """Test helpers.send_email_report() logs a success message when an email is sent successfully.

    Args:
        reports_test_dir (str): The relative path to the test reports directory.
        friends_bot_likelihood_scores (list): A list containing the bot likelihood scores for each Twitter friend.
        _get_datetime (str): A string representing the current datetime.
        email (str): A email provided by the pytest email fixture.
        username (str): A username provided by the pytest username fixture.
        caplog: A pytest caplog fixture used to examine application log messages.
    """
    # Get email credentials
    email_creds = helpers.get_env_vars(
        [
            "EMAIL_SERVER_DOMAIN",
            "EMAIL_SERVER_PORT",
            "EMAIL_SENDER_ADDRESS",
            "EMAIL_SENDER_PASSWORD",
        ]
    )
    # Create test reports directory
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
        email_server=email_creds["EMAIL_SERVER_DOMAIN"],
        email_server_port=int(email_creds["EMAIL_SERVER_PORT"]),
        email_sender_addr=email_creds["EMAIL_SENDER_ADDRESS"],
        email_sender_pass=email_creds["EMAIL_SENDER_PASSWORD"],
        email_recipient_addr=email,
        report_file_path=report_file_path,
        username=username,
    )
    assert (
        f"Sent email to: {email} with the friends bot likelihood report attached."
        in caplog.text
    )
