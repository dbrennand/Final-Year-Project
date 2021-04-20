"""Declare global fixtures for pytest.

The following code configures:

1. Configure Loguru handler when running pytest.

2. Configure pytest's caplog fixture to be able to capture Loguru log messages.
        Code taken from: https://loguru.readthedocs.io/en/stable/resources/migration.html#making-things-work-with-pytest-and-caplog

3. Add --email (required) and --username (optional) CLI options to pytest.
"""
import logging
import pytest
import sys
from _pytest.logging import caplog as _caplog
from loguru import logger

config = {
    "handlers": [
        {"sink": sys.stdout, "backtrace": False, "diagnose": False},
    ]
}

logger.configure(**config)


@pytest.fixture
def caplog(_caplog):
    class PropogateHandler(logging.Handler):
        def emit(self, record):
            logging.getLogger(record.name).handle(record)

    handler_id = logger.add(PropogateHandler(), format="{message} {extra}")
    yield _caplog
    logger.remove(handler_id)


def pytest_addoption(parser):
    parser.addoption("--email", action="store")
    parser.addoption("--username", action="store")


@pytest.fixture
def email(request):
    return request.config.getoption("--email")


@pytest.fixture
def username(request):
    return request.config.getoption("--username")
