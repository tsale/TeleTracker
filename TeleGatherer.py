import requests
import time
import pprint
import argparse
import multiprocessing
from helpers.TeleTexter import send_telegram_message
from helpers.TeleViewer import process_messages


def parse_dict(title, dictionary):
  result = f"{title}:\n"
  for key, value in dictionary.items():
    if isinstance(value, dict):
      result += '\n'.join(f"- {k}: {v}" for k, v in value.items())
    else:
      result += f"- {key}: {value}\n"
  return result + "\n"


def deleteMessage(bot_token, chat_id, message_id):
  url = f"https://api.telegram.org/bot{bot_token}/deleteMessage"
  data = {"chat_id": chat_id, "message_id": message_id}
  response = requests.post(url, data=data)
  return response.json()


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
    message_id = response.get('result').get('message_id')
    deleteMessage(bot_token, chat_id, message_id)
    return message_id
  else:
    print("Error: Unable to retrieve latest message id: ",
          response.get("description"))
    return None


def main(bot_token, chat_id):
  # Retrieve information and print in a pretty format
  can_read = get_bot_info(bot_token).get('result',
                                         {}).get('can_read_all_group_messages',
                                                 False)
  print(parse_dict("Bot Information", get_bot_info(bot_token)))
  print(parse_dict("Chat Information", get_chat_info(bot_token, chat_id)))
  print(
      parse_dict("Chat Administrators",
                 get_chat_administrators(bot_token, chat_id)))
  print(
      parse_dict("My Default Administrator Rights",
                 get_My_Default_AdministratorRights(bot_token, chat_id)))
  print(
      parse_dict("Available Bot Commands", get_my_commands(chat_id,
                                                           bot_token)))
  print(
      parse_dict("Chat Member Count",
                 get_chat_member_count(bot_token, chat_id)))

  while True:
    print("\nOptions:")
    print("1. Monitor for new messages from a different bot")
    print("2. Send a message to the malicious telegram channel")
    print("3. Spam the malicious telegram channel with a specific message")
    print(
        "4. Delete all messages from the malicious telegram channel that are sent within 24 hours"
    )
    print(
        "5. Get approximate number of messages on the malicious telegram channel"
    )
    print("6. Get messages from the malicious telegram channel")
    print("7. EXIT")
    choice = input("\nEnter your choice: ")
    if choice == '1':
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

    elif choice == '2':
      message = input("Enter the message you want to send: ")
      response = send_telegram_message(bot_token, chat_id, message)
      if response.get("ok") == True:
        print("Message sent. Response:")
        pprint.pprint(response)

    elif choice == '3':
      message = input("Enter the message you want to spam: ")
      processes = []
      for _ in range(1000000000):  # Adjust the number of processes as needed
        p = multiprocessing.Process(target=send_telegram_message,
                                    args=(bot_token, chat_id, message))
        p.start()
        processes.append(p)

      for p in processes:
        p.join()

    elif choice == '4':
      x = get_latest_messageid(bot_token, chat_id)
      try:
        consecutive_not_found = 0
        deleted_num = 0
        while consecutive_not_found < 100:
          max_retries = 5
          for i in range(max_retries):
            try:
              if x is None:
                break
              response = deleteMessage(bot_token, chat_id, x)
              if response.get("ok") == True:
                print(f"Deleted message {x}")
                x -= 1
                deleted_num += 1
                consecutive_not_found = 0
              elif response.get("ok") == False and response.get(
                  "description"
              ) == "Bad Request: message can't be deleted for everyone":
                print(
                    f"Message {x} is an old message. You can only delete messages that are within 24 hours."
                )
                x -= 1
              elif response.get("ok") == False:
                print(f"Message {x} not found.")
                consecutive_not_found += 1
                x -= 1
            except Exception as e:
              print(
                  f"Error: {e}. Attempt {i+1} of {max_retries}. Retrying in 5 seconds..."
              )
              time.sleep(5)
          time.sleep(0.04)  # Delay to respect rate limits, adjust as needed
        print(f"Deleted {deleted_num} messages from the malicious channel.")
      except Exception as e:
        print(f"Error: {x}")

    elif choice == '5':
      message_id = get_latest_messageid(bot_token, chat_id)
      if message_id is not None:
        print(
            f"Approximate number of messages on the malicious channel: {message_id}"
        )
      else:
        print(message_id)

    elif choice == '6':
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
            "Would you like to start from a specific message_id? (y/n): ")
        if question.lower() == 'y':
          message_id = int(
              input(f"Enter the message_id offset to start from: "))
        if message_id is not None:
          process_messages(bot_token, chat_id, num_messages, message_id)
        else:
          print(message_id)
      except Exception as e:
        print(f"Error: {e}")

    elif choice == '7':
      print("Exiting...")
      break
    else:
      print("Invalid choice. Please try again.")


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Telegram Bot Script")
  parser.add_argument("-t", "--bot_token", help="Telegram Bot Token")
  parser.add_argument("-c", "--chat_id", help="Telegram Chat ID", type=int)
  args = parser.parse_args()

  main(args.bot_token, args.chat_id)
