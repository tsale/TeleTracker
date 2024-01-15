import requests
import time
import pprint
import argparse

def create_invite_link(chat_id, bot_token):
  url = f"https://api.telegram.org/bot{bot_token}/createChatInviteLink"
  data = {"chat_id": chat_id}
  response = requests.get(url, data=data)
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


def main(bot_token, chat_id):
  # Retrieve information and print in a pretty format
  bot_info = get_bot_info(bot_token)
  can_read = bot_info.get('result', {}).get('can_read_all_group_messages',
                                            False)
  print("\nBot Information:")
  pprint.pprint(bot_info, indent=4, width=50)

  chat_info = get_chat_info(bot_token, chat_id)
  print("\nChat Information:")
  pprint.pprint(chat_info, indent=4, width=50)

  chat_admins = get_chat_administrators(bot_token, chat_id)
  print("\nChat Administrators:")
  pprint.pprint(chat_admins, indent=4, width=50)

  default_admin_rights = get_My_Default_AdministratorRights(
      bot_token, chat_id)
  print("\nMy Default AdministratorRights:")
  pprint.pprint(default_admin_rights, indent=4, width=50)

  get_available_commands = get_my_commands(chat_id, bot_token)
  print("\nAvailable bot Commands:")
  pprint.pprint(get_available_commands, indent=4, width=50)

  member_count = get_chat_member_count(bot_token, chat_id)
  print("\nChat Member Count:")
  pprint.pprint(member_count, indent=4, width=50)

  if can_read:
    answer = input(
        "Looks like the bot is misconfigured and has administrator permissions, choose what you'd like to do from the list below: )"
    )
    
    while True:
      print("\nOptions:")
      print("1. Monitor for new messages")
      print("2. Create a chat invite link ;) ")
      print()
      choice = input("Enter your choice (1 or 2): ")

      if choice == '1':
          offset = None  # Variable to keep track of the last update ID
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
      elif choice == '2':
        createInviteLink = create_invite_link(chat_id, bot_token)
        print("\nChat Invite Link:")
        pprint.pprint(createInviteLink, indent=4, width=50)
      else:
          print("Invalid choice. Please try again.")
  else:
    print("The bot does not have permission to read all group messages.")


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Telegram Bot Script")
  parser.add_argument("-t", "--bot_token", help="Telegram Bot Token")
  parser.add_argument("-c", "--chat_id", help="Telegram Chat ID")
  args = parser.parse_args()

  main(args.bot_token, args.chat_id)