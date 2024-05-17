# Telegram Breach Notification Bot

This repository contains a Python-based Telegram bot that helps users check for recent data breaches and whether their email addresses have been compromised. The bot provides the following commands:
- `/start` - Starts the bot
- `/breaches` - Shows the recent data breaches in the last 30 days
- `/breached [email]` - Checks if an email has been pwned
- `/help` - Shows a help message with available commands

## Features
- Fetches recent data breaches from an external API.
- Checks if an email address has been compromised.
- Sends notifications with detailed breach information, including logos and descriptions.
- Supports HTML formatting in messages.

## Requirements
- Python 3.x
- `requests` library
- `python-dotenv` library

## Setup
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/telegram-breach-bot.git
    cd telegram-breach-bot
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add your Telegram bot token:
    ```env
    TOKEN=your_telegram_bot_token
    ```

4. Deploy the bot using AWS Lambda or run it locally using the `telegram_bot.py` script.

## Usage
### Running the Bot Locally
To run the bot locally, execute the following command:
```sh
python telegram_bot.py
```

## Deploying to AWS Lambda
To deploy the bot to AWS Lambda, package the Lambda.py script and its dependencies and upload it to your Lambda function. Configure the Lambda function to be triggered by API Gateway or another event source.

## Commands
```
/start - Start the bot and receive a welcome message.
/breaches - Get a list of recent data breaches from the last 30 days.
/breached [email] - Check if the provided email address has been pwned.
/help - Show a help message with available commands.
```