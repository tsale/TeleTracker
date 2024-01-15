import requests
import time
import pprint
import argparse
from TeleTexter import send_telegram_message


def parse_dict(title, dictionary):
  result = f"{title}:\n"
  for key, value in dictionary.items():
    if isinstance(value, dict):
      result += '\n'.join(f"- {k}: {v}" for k, v in value.items())
    else:
      result += f"- {key}: {value}\n"
  return result + "\n"


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
    print("4. Delete all messages from the malicious telegram channel")
    print("5. EXIT")
    choice = input("\nEnter your choice: ")
    if choice == '1':
      offset = None  # Variable to keep track of the last update ID
      if can_read:
        print("\t [*] Administrator persmission granted. Monitoring for new messages....")
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
      send_telegram_message(bot_token, chat_id, message)
      print("Message sent successfully!")
    elif choice == '3':
      message = input("Enter the message you want to spam: ")
      try:
        while True:
          response = send_telegram_message(bot_token, chat_id, message)
          if response.status_code == 200:
            print("\n[+] Message sent successfully!")
          time.sleep(0.04)  # Delay to respect rate limits, adjust as needed
      except KeyboardInterrupt:
        print("Spamming interrupted. Going back to options.")
    elif choice == '4':
      x = 0
      consecutive_not_found = 0
      url = f"https://api.telegram.org/bot{bot_token}/deleteMessage"
      while consecutive_not_found < 20:
        data = {"chat_id": chat_id, "message_id": x}
        response = requests.post(url, data=data)
        x += 1
        if response.status_code == 200:
          print("Message deleted successfully!")
          consecutive_not_found = 0
        elif response.status_code == 400:
          consecutive_not_found += 1
        time.sleep(0.04)  # Delay to respect rate limits, adjust as needed
    elif choice == '5':
      print("Exiting...")
      break
    else:
      print("Invalid choice. Please try again.")


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Telegram Bot Script")
  parser.add_argument("-t", "--bot_token", help="Telegram Bot Token")
  parser.add_argument("-c", "--chat_id", help="Telegram Chat ID")
  args = parser.parse_args()

  main(args.bot_token, args.chat_id)
