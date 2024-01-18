import requests
import argparse
import pprint
import time


def send_telegram_message(bot_token, chat_id, message):
  """
    Sends a message to a specified Telegram channel.
    """
  url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
  data = {"chat_id": chat_id, "text": message}
  response = requests.post(url, data=data)
  if response.json().get("ok") == True:
    print(f"Message sent successfully! -> message_id: {response.json().get('result').get('message_id')}")
  return response.json()


def main(bot_token, chat_id, message, spam):
  if spam:
    while True:
      response = send_telegram_message(bot_token, chat_id, message)
      print("Message sent. Response:")
      pprint.pprint(response)        
      time.sleep(0.04)  # Delay to respect rate limits, adjust as needed
  else:
    response = send_telegram_message(bot_token, chat_id, message)
    print("Message sent. Response:")
    pprint.pprint(response)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description="Send a message to a Telegram channel")
  parser.add_argument("-t", "--bot_token", help="Telegram Bot Token")
  parser.add_argument("-c", "--chat_id", help="Telegram Chat ID")
  parser.add_argument("-m", "--message", help="Message to send")
  parser.add_argument("--spam", help="Send messages continuously", action="store_true")

  args = parser.parse_args()

  main(args.bot_token, args.chat_id, args.message, args.spam)
