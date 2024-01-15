# TeleTracker

This repository contains Python scripts, `TeleTexter.py` and `TeleGatherer.py`, designed to assist analysts in tracking and disrupting active malware campaigns that use Telegram for command and control (C2) communications.

### TeleTexter.py

`TeleTexter.py` is a script for sending messages to a specified Telegram channel. It can be used to send singular messages or continuously send messages at a rate of 25 messages per second. This script can be utilized in counter-operation strategies to disrupt C2 channels used by malware.

### TeleGatherer.py

`TeleGatherer.py` is a script for gathering information regarding the channels of which the bots operate. It provides functionalities to:
- Retrieve basic information about a bot.
- Gather details about a specific chat, including chat administrators and member count.
- Information about the user behind the telegram channel, including Username and provided first and last name.
- Optionally, read all group messagesn and creating an invite link to access the channel if the bot has the necessary permissions.

This script is useful for analysts who need to monitor Telegram channels, collect information and track adversaries. 

## Installation

To use these scripts, Python must be installed on your system, along with the `requests` library.

1. Clone the repository:\
`git clone https://github.com/yourusername/TeleTracker.git`

2. Install the required Python package:\
`pip install requests`

## Usage

### TeleTexter.py

To send a message to a Telegram channel:

`python TeleTexter.py -t YOUR_BOT_TOKEN -c YOUR_CHAT_ID -m "Your message here"`

To send messages continuously:

`python TeleTexter.py -t YOUR_BOT_TOKEN -c YOUR_CHAT_ID -m "Your message here" --spam`


### TeleGatherer.py

To gather intelligence from a Telegram channel:\

`python TeleGatherer.py -t YOUR_BOT_TOKEN -c YOUR_CHAT_ID`


## Disclaimer

Use these tools responsibly. They are intended for analysis and research purposes only. Ensure compliance with all applicable laws and Telegram's terms of service.
