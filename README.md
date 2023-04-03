# Child Diary Telegram Bot

This Python code connects to the [Child Diary API](https://childdiary.net/), retrieves the latest entry, and publishes it to a Telegram chat. The code is designed to run indefinitely, checking for new entries every hour.

## Requirements

* Python 3.x
* `requests` library
* `telegram` library
* `beautifulsoup4` library

## Setup

1. Clone the repository to your local machine.
2. Install the required libraries using `pip install -r requirements.txt`.
3. Create a Telegram bot and obtain its token.
4. Create a Telegram chat and obtain its ID.
5. Create a Child Diary account and obtain your login credentials.
6. Set environment variables for `CD_EMAIL`, `CD_PASSWORD`, `TELEGRAM_TOKEN`, and `TELEGRAM_CHAT_ID`.

## How to Use

1. Run the script using `python main.py`.
2. The bot will check for new entries every hour.
3. If a new entry is found, it will be published to the specified Telegram chat.

## Notes

* The Child Diary API is not an official API and is subject to change without notice.
* Use of this code may violate the Child Diary terms of service.
* This code is provided for educational purposes only. Use at your own risk.
