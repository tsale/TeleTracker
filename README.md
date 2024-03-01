# TeleTracker

This repository contains Python scripts, `TeleTexter.py`, `TeleGatherer.py` and `TeleViewer.py`, designed to assist analysts in tracking and disrupting active malware campaigns that use Telegram for command and control (C2) communications.

### TeleGatherer.py

`TeleGatherer.py` is the main script for gathering intelligence on the activities of threat actors and the data they collect from compromised hosts. It has been updated with new features and improvements:

- ✅ **View Channel Messages & Download Content**
  - Save content in current working directory under new folder named 'downloads'.
  - Supports the download of documents, photos, videos, etc.

- ✅ **Send Documents via Telegram**
  - Optionally send a message.
  - Supports all Telegram file types.
  - Auto-detects MIME type.

- ✅ **Message Selection**
  - Choose a specified number of messages or a specific message_id for download.
  - Download is **ALWAYS** from newest to oldest message.

- ✅ **Log Saving**
  - Pretty text with basic info under <bot_name>.txt.
  - Full JSON dumps of each message under <bot_name>.json.

- ✅ **Bot Information Retrieval**
  - Get info on bot and owner.
  - Includes channel-related details.

- ✅ **Newest Added Feature/Enhancement**
  - Send files functionality.

- ✅ **Optional Menu**
  - **MONITOR:** Read new messages.
  - **DISRUPT:** Delete messages from malicious channels.
  - **DISRUPT:** Spam channels at a high rate with the message of your choice.

> [!NOTE]
> This script is intended for threat intelligence analysts or researchers who want to monitor, collect, and track adversaries using Telegram for C2 communication.

## Installation

To use these scripts, Python must be installed on your system, along with the `requests` library.

1. Clone the repository:\
```git clone https://github.com/tsale/TeleTracker.git```

2. Install the required Python package:\
`pip install -r requirements`

## Usage

### TeleTexter.py

To send a message to a Telegram channel:

`python TeleTexter.py -t YOUR_BOT_TOKEN -c YOUR_CHAT_ID -m "Your message here"`

To send messages continuously:

`python TeleTexter.py -t YOUR_BOT_TOKEN -c YOUR_CHAT_ID -m "Your message here" --spam`

### Introducing Televiewer.py

`Televiewer.py` is the latest tool, allowing you to view and download all messages and media from the threat actor-controlled telegram channel. You can use this feature by selecting the number 6 from the initial menu after running `TeleGathere.py`. With `Televiewer.py` features, you can:

- View all channel messages and download all uploaded content, including documents, photos, videos, and other media. All downloaded content is saved in a `downloads` directory.
- Specify the number of messages to download, from the newest to the oldest.
- Save all text in two formats: clean, readable text with basic info saved in a Txt file and a comprehensive list of every message saved in a JSON file.

To use `Televiewer.py`, create a [Telegram API](https://core.telegram.org/api/obtaining_api_id) and add your `API_hash` and `API_id` to the `.env` file. in the below format:

```
API_ID="XXX"
API_HASH="XXX"
```


### TeleGatherer.py

To gather intelligence from a Telegram channel:

`python TeleGatherer.py -t YOUR_BOT_TOKEN -c YOUR_CHAT_ID`

## Recent Updates

- Ability to view and download all types of media from channels.
- Option to select the number of messages for downloading.
- Dual format text saving: pretty text and full JSON dumps.
- Numerous improvements and bug fixes to enhance existing features.

## Disclaimer

Use these tools responsibly. They are intended for analysis and research purposes only. Ensure compliance with all applicable laws and Telegram's terms of service.
