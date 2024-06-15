import requests
import time
import pprint
import argparse
import multiprocessing
import mimetypes
from helpers.TeleTexter import send_telegram_message
from helpers.TeleViewer import process_messages


def parse_dict(title, dictionary):
    result = f"{title}:\n"
    for key, value in dictionary.items():
        if isinstance(value, dict):
            result += "\n".join(f"- {k}: {v}" for k, v in value.items())
        else:
            result += f"- {key}: {value}\n"
    return result + "\n"


def delete_messages(bot_token, chat_id, message_id):
    try:
        response = deleteMessage(bot_token, chat_id, message_id)
        if response.get("ok") == True:
            print(f"Deleted message {message_id}")
            message_id -= 1
        elif (
            response.get("ok") == False
            and response.get("description")
            == "Bad Request: message can't be deleted for everyone"
        ):
            print(
                f"Message {message_id} is an old message. You can only delete messages that are within 24 hours."
            )
        elif response.get("ok") == False:
            print(f"Message {message_id} not found.")
    except Exception as e:
        print(f"Error: {message_id}")


def deleteMessage(bot_token, chat_id, message_id):
    url = f"https://api.telegram.org/bot{bot_token}/deleteMessage"
    data = {"chat_id": chat_id, "message_id": message_id}
    response = requests.post(url, data=data)
    return response.json()


def send_file_to_telegram_channel(bot_token, chat_id, file_path):
    try:
        mime_type = mimetypes.guess_type(file_path)[0]
        file_type = "document"  # default to document

        if mime_type:
            if "audio" in mime_type:
                file_type = "audio"
            elif "video" in mime_type:
                file_type = "video"
            elif "image" in mime_type:
                file_type = "photo"

        file_type_methods = {
            "document": "sendDocument",
            "photo": "sendPhoto",
            "audio": "sendAudio",
            "video": "sendVideo",
            "animation": "sendAnimation",
            "voice": "sendVoice",
            "video_note": "sendVideoNote",
        }

        url = f"https://api.telegram.org/bot{bot_token}/{file_type_methods[file_type]}"
        with open(file_path, "rb") as file:
            files = {file_type: file}
            message = input(
                "Enter the message to send with the file (press enter to skip): "
            )
            data = {"chat_id": chat_id, "caption": message}
            response = requests.post(url, files=files, data=data)
            return response.json()
    except Exception as e:
        print(f"An error occurred while trying to send the file: {e}")


def get_my_commands(chat_id, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getMyCommands"
    data = {"chat_id": chat_id}
    response = requests.get(url, data=data)
    return response.json()


def get_updates(bot_token, offset=None, timeout=30):
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates?timeout={timeout}"
    if offset:
        url += f"&offset={offset}"
    response = requests.get(url)
    return response.json()


def get_bot_info(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    response = requests.get(url)
    return response.json()


def get_My_Default_AdministratorRights(bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/getMyDefaultAdministratorRights"
    data = {"chat_id": chat_id}
    response = requests.get(url, data=data)
    return response.json()


def get_chat_info(bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/getChat"
    data = {"chat_id": chat_id}
    response = requests.post(url, data=data)
    return response.json()


def get_chat_administrators(bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/getChatAdministrators"
    data = {"chat_id": chat_id}
    response = requests.post(url, data=data)
    return response.json()


def get_chat_member_count(bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/getChatMembersCount"
    data = {"chat_id": chat_id}
    response = requests.post(url, data=data)
    return response.json()


def get_latest_messageid(bot_token, chat_id):
    response = send_telegram_message(bot_token, chat_id, ".")
    if response.get("ok") == True:
        message_id = response.get("result").get("message_id")
        deleteMessage(bot_token, chat_id, message_id)
        return message_id
    else:
        print(
            "Error: Unable to retrieve latest message id: ", response.get("description")
        )
        return None


def main(bot_token, chat_id):
    # Retrieve information and print in a pretty format
    can_read = (
        get_bot_info(bot_token)
        .get("result", {})
        .get("can_read_all_group_messages", False)
    )
    if not args.silent:
        print(parse_dict("Bot Information", get_bot_info(bot_token)))
        print(parse_dict("Chat Information", get_chat_info(bot_token, chat_id)))
        print(
            parse_dict(
                "Chat Administrators", get_chat_administrators(bot_token, chat_id)
            )
        )
        print(
            parse_dict(
                "My Default Administrator Rights",
                get_My_Default_AdministratorRights(bot_token, chat_id),
            )
        )
        print(parse_dict("Available Bot Commands", get_my_commands(chat_id, bot_token)))
        print(
            parse_dict("Chat Member Count", get_chat_member_count(bot_token, chat_id))
        )
    if args.info:
        exit()
    while True:
        print("\nOptions:")
        print("1. Monitor for new messages from a different bot")
        print("2. Send a message to the malicious telegram channel")
        print("3. Spam the malicious telegram channel with a specific message")
        print(
            "4. Delete all messages from the malicious telegram channel that are sent within 24 hours\n"
        )
        print("5. Get approximate number of messages on the malicious telegram channel")
        print("6. Download ALL messages from the malicious telegram channel")
        print("7. Send a file to the malicious telegram channel\n")
        print("8. EXIT")
        choice = input("\nEnter your choice: ")
        if choice == "1":
            offset = None  # Variable to keep track of the last update ID
            if can_read:
                print(
                    "\t [*] Administrator persmission granted. Monitoring for new messages...."
                )
                while True:
                    try:
                        updates = get_updates(bot_token, offset)
                        for update in updates.get("result", []):
                            print("Received Update:")
                            pprint.pprint(update, indent=4, width=50)

                            # Update the offset to only receive new updates
                            offset = update["update_id"] + 1
                    except KeyboardInterrupt:
                        print("Monitoring interrupted. Going back to options.")
                        break
                    time.sleep(1)
            else:
                print("Bot does not have permission to read messages.")

        elif choice == "2":
            message = input("Enter the message you want to send: ")
            response = send_telegram_message(bot_token, chat_id, message)
            if response.get("ok") == True:
                print("Message sent. Response:")
                pprint.pprint(response)

        elif choice == "3":
            message = input("Enter the message you want to spam: ")
            processes = []
            for _ in range(1000000000):  # Adjust the number of processes as needed
                p = multiprocessing.Process(
                    target=send_telegram_message, args=(bot_token, chat_id, message)
                )
                p.start()
                processes.append(p)

            for p in processes:
                p.join()

        elif choice == "4":
            message_id = get_latest_messageid(bot_token, chat_id)
            processes = []
            for _ in range(1000000000):  # Adjust the number of processes as needed
                p = multiprocessing.Process(
                    target=delete_messages, args=(bot_token, chat_id, message_id)
                )
                p.start()
                processes.append(p)
                message_id -= 1

            for p in processes:
                p.join()

        elif choice == "5":
            message_id = get_latest_messageid(bot_token, chat_id)
            if message_id is not None:
                print(
                    f"Approximate number of messages on the malicious channel: {message_id}"
                )
            else:
                print(message_id)

        elif choice == "6":
            try:
                message_id = get_latest_messageid(bot_token, chat_id)
                print(f"\t\n TOTAL NUMBER OF MESSAGES: ~{message_id}\n")
                num_messages = input(
                    "Press ENTER to retreive all messages or enter a number (Downloading from Newest to Oldest): "
                )
                if num_messages == "":
                    num_messages = message_id
                else:
                    num_messages = int(num_messages)
                question = input(
                    "Would you like to start from a specific message_id? (y/n): "
                )
                if question.lower() == "y":
                    message_id = int(
                        input(f"Enter the message_id offset to start from: ")
                    )
                if message_id is not None:
                    process_messages(bot_token, chat_id, num_messages, message_id)
                else:
                    print(message_id)
            except Exception as e:
                print(f"Error: {e}")
        elif choice == "7":
            file_path = input("Enter the absolute file path: ")
            response = send_file_to_telegram_channel(bot_token, chat_id, file_path)
            if response.get("ok") == True:
                print("File sent. Response:")
                pprint.pprint(response)
            else:
                print("Error: Unable to send file: ", response.get("description"))
        elif choice == "8":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


# Check a file for the bot token and chat id pair it is stored in the file in the form of bot_token:chat_id, then print a message asking if you are sure you want to continue. Otherwise continue and add the bot token and chat id to the file in the form of bot_token:chat_id and continue.
def check_file_for_token_and_chat_id(file_path, bot_token, chat_id):
    with open(file_path, "r") as file:
        for line in file:
            if line.strip() == f"{bot_token}:{chat_id}":
                return True
    return False


def add_token_and_chat_id_to_file(file_path, bot_token, chat_id):
    with open(file_path, "a") as file:
        file.write(f"{bot_token}:{chat_id}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Telegram Bot Script")
    parser.add_argument("-t", "--bot_token", help="Telegram Bot Token")
    parser.add_argument(
        "-i", "--info", help="Get Bot Information and exit", action="store_true"
    )
    parser.add_argument("-c", "--chat_id", help="Telegram Chat ID", type=int)
    parser.add_argument(
        "-s",
        "--silent",
        help="Silent mode, no prompts, just show the information and exit",
        action="store_true",
    )
    args = parser.parse_args()

    file_path = ".bot-history"  # Replace with the actual file path

    if check_file_for_token_and_chat_id(file_path, args.bot_token, args.chat_id):
        print("Bot token and chat ID pair already exists in the file.")
        response = input("Are you sure you want to continue? (y/n): ")
        if response.lower() != "y":
            exit()
    else:
        add_token_and_chat_id_to_file(file_path, args.bot_token, args.chat_id)

    main(args.bot_token, args.chat_id)
