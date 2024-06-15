import pyrogram
import json
from dotenv import load_dotenv
import os
import random

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")


def get_file_info(data):
    media_type = ""
    random_numbers = [random.randint(1, 100) for _ in range(6)]
    # print("data.media value:", data.media)
    if data.media is not None:
        try:
            for key in [
                "MessageMediaType.DOCUMENT",
                "MessageMediaType.PHOTO",
                "MessageMediaType.VIDEO",
                "MessageMediaType.LOCATION",
                "MessageMediaType.VOICE",
                "MessageMediaType.AUDIO",
                "MessageMediaType.STICKER",
                "MessageMediaType.ANIMATION",
            ]:
                if key in str(data):
                    media_type = key
                    # print("Media_type found:", media_type)
                    break
            if media_type == "MessageMediaType.DOCUMENT":
                return (data.document.file_id, data.document.file_name)
            elif media_type == "MessageMediaType.PHOTO":
                return (data.photo.file_id, f"{random_numbers}.png")
            elif media_type == "MessageMediaType.VIDEO":
                return (data.video.file_id, data.video.file_name)
            elif media_type == "MessageMediaType.LOCATION":
                return (data.location.file_id, data.location.file_name)
            elif media_type == "MessageMediaType.VOICE":
                return (data.voice.file_id, data.voice.file_name)
            elif media_type == "MessageMediaType.AUDIO":
                return (data.audio.file_id, data.audio.file_name)
            elif media_type == "MessageMediaType.STICKER":
                return (data.sticker.file_id, data.sticker.file_name)
            elif media_type == "MessageMediaType.ANIMATION":
                return (data.animation.file_id, data.animation.file_name)
            else:
                return (None, None)
        except Exception as e:
            print(f"Error: {e}")
            return (None, None)


def parse_and_print_message(message):
    print("=" * 20 + "\n")
    message_dict = message.__dict__
    for key, value in message_dict.items():
        if value not in [None, False]:
            print(f"{key}: {value}")
    print("\n")
    print("=" * 20 + "\n")


def process_messages(bot_token, chat_id, num_messages, message_id):
    directory = f"sessions/{chat_id}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    bot_token_filename = bot_token.replace(":", "_").replace("/", "_")
    bot_token_filename = f"{directory}/{bot_token_filename}.session"
    app = pyrogram.Client(bot_token_filename, api_id, api_hash)

    async def main(num_messages, message_id):
        try:
            # Calculate the counter to get the correct number of messages. We do this so we can iterate through the messages in reverse order from the latest message.
            counter = message_id - num_messages
            while message_id >= counter:
                message_id -= 1
                async with app:
                    messages = await app.get_messages(chat_id, message_id)
                    if messages.date is None:
                        # Display the message_id not found every 10 messages
                        if message_id % 10 == 0:
                            print(f"[-] Message_id {message_id} not found")
                        counter -= 1
                        pass
                    else:
                        parse_and_print_message(messages)
                        if messages.media is not None:
                            file_id, file_name = get_file_info(messages)
                            if messages.from_user is not None:
                                file_name = f"downloads/{messages.from_user.username}/{message_id}_{file_name}"
                            else:
                                file_name = (
                                    f"downloads/{chat_id}/{message_id}_{file_name}"
                                )

                            # download the file
                            # Keep track of the progress while downloading
                            async def progress(current, total):
                                if total != 0:
                                    print(f"{current * 100 / total:.1f}%")
                                else:
                                    print(
                                        f"[*] Download of {file_name.split('/')[-1]} is complete!"
                                    )

                            await app.download_media(
                                file_id,
                                file_name=file_name,
                                progress=progress,
                            )
                        # save to file
                        if messages.from_user is not None:
                            username = messages.from_user.username
                            directory = f"Downloads/{username}/logs"
                            if not os.path.exists(directory):
                                os.makedirs(directory)
                            with open(f"{directory}/{username}_bot.txt", "a") as file:
                                file.write(f"Message ID: {messages.id}\n")
                                file.write(
                                    f"From User ID: {messages.from_user.id} - Username: {messages.from_user.username}\n"
                                )
                                file.write(f"Date: {messages.date}\n")
                                file.write(f"Text: {messages.text}\n")
                                file.write(f"Reply_markup: {messages.reply_markup}\n\n")
                            # Save the whole message to a file
                            with open(f"{directory}/{username}_bot.json", "a") as file:
                                file.write(str(messages))
                        else:
                            directory = f"Downloads/{chat_id}/logs"
                            if not os.path.exists(directory):
                                os.makedirs(directory)
                            with open(f"{directory}/{chat_id}_bot.txt", "a") as file:
                                file.write(f"Message ID: {messages.id}\n")
                                file.write(f"Date: {messages.date}\n")
                                file.write(f"Text: {messages.text}\n")
                                file.write(f"Reply_markup: {messages.reply_markup}\n\n")
                            # Save the whole message to a file
                            with open(f"{directory}/{chat_id}_bot.json", "a") as file:
                                file.write(str(messages))
        except AttributeError as e:
            print(f"Error: {e}")
            pass
        except Exception as e:
            print(f"Error: {e}")
            pass

    try:
        app.run(main(num_messages, message_id))
    except KeyboardInterrupt:
        print("\nStopping...")
        app.disconnect()
        pass
