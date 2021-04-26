# Final-Year-Project

## Introduction

This application was developed as part of my final year project for university.

The purpose of the application is to identify potential bots that a Twitter user is following. Accounts that a Twitter user is following are known as [friends](https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-friends-ids).

The application does this by generating a report which contains likelihood scores for a Twitter user's friends being a bot. The report is sent to the Twitter user via email.

The scores are provided by leveraging the [Botometer API](https://rapidapi.com/OSoMe/api/botometer-pro/details). You can find more information about Botometer [here](https://botometer.osome.iu.edu/faq).

> [!NOTE]
>
> Please note that this application is not affiliated with Twitter or the Botometer project.

## Dependencies

This application is written in **Python 3.9** and relies on the following dependencies:

```
[packages]
botometer = "1.6"
tweepy = "3.10.0"
loguru = "0.5.3"
jinja2 = "2.11.3"
pycountry = "20.7.3"
faker = "8.1.1"

[dev-packages]
black = "20.8b1"
pytest = "6.2.3"
pytest-cov = "2.11.1"
pytest-mock = "3.5.1"

[requires]
python_version = "3.9"
```

These dependencies can be installed using either: `pipenv install` or `pip install -r requirements.txt`.

## Prerequisites

Before using the project's application, credentials for the following are required:

* The Twitter API

* The Botometer API

* An email server and account

### Twitter API Credentials

The project's application uses the Twitter API to collect a Twitter user's friends.

To get access to the Twitter API, a developer account is needed. You can apply for one [here](https://developer.twitter.com/en/apply-for-access). You can find more information about this process [here](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api).

Once you have a developer account, go to the [developer portal](https://developer.twitter.com/en/portal/dashboard) to create an application.

When creating the application, provide a unique *name* and click **Complete**. The application's API key and secret will be shown (aka. consumer key and consumer secret). Store them somewhere safe as they will be needed in the [final step](#Exporting-Credentials).

### Botometer API Credentials

The project's application uses the [Botometer API](https://rapidapi.com/OSoMe/api/botometer-pro/details) to collect bot likelihood scores for a Twitter user's friends.

To get access to the Botometer API, a RapidAPI account is needed. You can create one [here](https://rapidapi.com/auth/sign-up).

Once you have a RapidAPI account, go to the Botometer API [pricing](https://rapidapi.com/OSoMe/api/botometer-pro/pricing) page and subscribe to the *Pro* or *Basic* plan.

> [!NOTE]
>
> The *Pro* plan requires a credit or debit card to be added to the RapidAPI account.

Once you have chosen a plan, go to the RapidAPI [developer dashboard](https://rapidapi.com/developer/apps) and go to security for the `default-application`. The application key (API key) will be shown. Store it somewhere safe as it will be needed in the [final step](#Exporting-Credentials).

### Email Credentials

> [!NOTE]
>
> The instructions below let the project's application send the report via email using **Google's SMTP servers** and a **Google** account.
>
> If you are using another email provider, you will need to find their own instructions on how to authenticate to their email servers.

At the time of writing (21/04/2021), Google's SMTP server domain is `smtp.gmail.com` and SSL port is `465`. For more information, see the *Use the Gmail SMTP server* heading in Google's [documentation](https://support.google.com/a/answer/176600?hl=en#zippy=%2Cuse-the-gmail-smtp-server).

Perform the steps below to generate an app password for a Google account. This will allow the project's application to send an email from the account.

> [!NOTE]
>
> To generate an app password for a Google account, 2-Step Verification must be set up on the account.
>
> Documentation on how to this can be found [here](https://support.google.com/accounts/answer/185839?hl=en&ref_topic=7189195).

1. Temporarily enable [*less secure app access*](https://myaccount.google.com/lesssecureapps) on the Google account.

    * You *may* need to sign in. Turn *Allow less secure apps* on.

2. Go to the [Google account](https://myaccount.google.com/) and select **Security**.

3. Under *Signing in to Google* section, select **App passwords**.

    * You *may* be prompted to enter the account password again.

4. In the *Select app* dropdown, select **Mail**.

5. In the *Select device* dropdown, select **Other (custom name)** and enter a friendly name for the app password.

6. Select **GENERATE**.

The app password will be shown. Store it somewhere safe as it will be needed in the [next step](#Exporting-Credentials).

> [!IMPORTANT]
>
> When finished using the project's application, make sure the app password is revoked from the Google account and *less secure app access* is disabled.
>
> Documentation on how to do this can be found [here](https://support.google.com/accounts/answer/6010255).

### Exporting Credentials

Once all the credentials have been collected, export them as environment variables to be accessed by the project's application.

1. Temporarily disable terminal command logging to prevent credential exposure:

    * Linux: `set +o history`

    > [!NOTE]
    >
    > Use the command: `set -o history` to re-enable terminal command logging.

    * Windows (PowerShell): `Set-PSReadlineOption -HistorySaveStyle SaveNothing`

    > [!NOTE]
    >
    > Use the command: `Set-PSReadlineOption -HistorySaveStyle SaveIncrementally` to re-enable terminal command logging.

2. Export the required credentials as environment variables:

    * Linux:

        ```bash
        export TWITTER_API_KEY="Enter the Twitter API key here."
        export TWITTER_API_SECRET="Enter the Twitter API secret here."
        export BOTOMETER_API_KEY="Enter the Botometer API key here."
        export EMAIL_SERVER_DOMAIN="smtp.gmail.com"
        export EMAIL_SERVER_PORT="465"
        export EMAIL_SENDER_ADDRESS="Enter the account email address here."
        export EMAIL_SENDER_PASSWORD="Enter the account app password here."
        ```

    * Windows (PowerShell):

        ```powershell
        $Env:TWITTER_API_KEY="Enter the Twitter API key here."
        $Env:TWITTER_API_SECRET="Enter the Twitter API secret here."
        $Env:BOTOMETER_API_KEY="Enter the Botometer API key here."
        $Env:EMAIL_SERVER_DOMAIN="smtp.gmail.com"
        $Env:EMAIL_SERVER_PORT="465"
        $Env:EMAIL_SENDER_ADDRESS="Enter the account email address here."
        $Env:EMAIL_SENDER_PASSWORD="Enter the account app password here."
        ```

## Usage

From the root of the repository, run the project's application using the command: `python ./src/main.py {Twitter Username} {Email Address}`

### CLI Usage

```
usage: main.py [-h] [-d] username email

Generates and emails a report containing bot likelihood scores for a Twitter user's friends.

positional arguments:
  username    The Twitter username to obtain friends for.
  email       The recipient email address to send the report to.

optional arguments:
  -h, --help  show this help message and exit
  -d, --demo  Flag to run the application in demo mode.
```

> [!IMPORTANT]
>
> Ensure you replace the placeholders ({}) with a Twitter username (**without** the "@" symbol) and an email address.
>
> For example:
>
> `python ./src/main.py dbrennanduk exampleemail@gmail.com`
>
> The above command would produce a bot likelihood report for *@dbrennanduk's* Twitter friends and send the report to *exampleemail@gmail.com*.

> [!NOTE]
>
> The application can be run in demo mode by providing either `-d` or `--demo` as an optional argument.

## Unit Tests

See the unit tests [README](./src/test/README.md) file.

## LICENSE

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) for details.
