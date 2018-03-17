import telebot
from bot import bussines
from bot import constants

bussines.Bot = telebot.TeleBot(constants.token)


@bussines.Bot.message_handler(commands=['start'])
def handle_start(message):
    if bussines.admin_checker(message):
        bussines.start(message)
    else:
        bussines.Bot.send_message(message.from_user.id, 'You do not have permissions')


@bussines.Bot.message_handler(content_types=['text'])
def handle_text(message):
    if bussines.admin_checker(message):
        if message.text == "stop":
            bussines.stop(message)

        elif message.text == "Add Video":
            bussines.add_video(message)

        elif message.text == "Generate Video":
            bussines.generate_video(message)

        elif (str(message.text).__contains__('https://www.youtube.com')) and bussines.Flag_Add:
            bussines.download_video(message)

        elif bussines.Flag_Generate:
            bussines.get_video(message)

        else:
            bussines.other(message)
    else:
        bussines.Bot.send_message(message.from_user.id, 'You do not have permissions')


try:
    b = bussines.Bot.polling(none_stop=True, interval=0)
    print(b)
except ConnectionError:
    print("Aborted Connection")
