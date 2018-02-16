import telebot
from bot import bussines
from bot import constants

bussines.Bot = telebot.TeleBot(constants.token)


@bussines.Bot.message_handler(commands=['start'])
def handle_start(message):
    bussines.start(message)


@bussines.Bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "stop":
        bussines.stop(message)

    elif message.text == "Add Video":
        bussines.add_video(message)

    elif message.text == "Generate Video":
        bussines.generate_video(message)

    elif (str(message.text).__contains__('https://www.youtube.com')) and bussines.Flag:
        bussines.download_video(message)

    elif bussines.Flag:
        bussines.get_video(message)

    else:
        bussines.other(message)


try:
    b = bussines.Bot.polling(none_stop=True, interval=0)
    print(b)
except ConnectionError:
    print("Aborted Connection")
