"""pytest's caplog fixture works with the standard logging module.

The following code configures the caplog fixture to be able to capture Loguru log messages.

Code taken from: https://loguru.readthedocs.io/en/stable/resources/migration.html#making-things-work-with-pytest-and-caplog
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
