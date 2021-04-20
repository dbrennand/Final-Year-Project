# Unit Tests

This directory contains unit tests for the modules located in the [modules](../modules) directory.

## Prerequisites

1. Ensure all the required environment variables are set from the [prerequisites](../../README.md#Prerequisites).

2. Ensure the requirements are installed using either:

    * `pipenv install --dev` or `pip install -r requirements.txt`

## Running the tests

To run the unit tests:

1. Ensure you have performed the [prerequisite](#Prerequisites) steps above.

2. Ensure your current working directory is the root of the repository (ie: `Final-Year-Project`)

3. Use the following command to run all the unit tests: `python -m pytest`

> [!NOTE]
>
> You can exclude a specific group of unit tests using markers. See [pytest.ini](../../pytest.ini) for available markers.
>
> You can also choose to run unit tests with a specific marker like so (runs only tests with "twitter" mark): `python -m pytest -m twitter`
