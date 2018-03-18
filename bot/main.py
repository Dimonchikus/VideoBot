import telebot
from bot import bussines
from bot import constants
import re

bussines.Bot = telebot.TeleBot(constants.token)


@bussines.Bot.message_handler(commands=['start'])
def handle_start(message):
    if bussines.user_checker(message.from_user.id):
        bussines.start(message)
    else:
        bussines.Bot.send_message(message.from_user.id, 'You do not have permissions')


@bussines.Bot.message_handler(content_types=['text'])
def handle_text(message):
    if bussines.user_checker(message.from_user.id):
        if message.text == "stop":
            bussines.stop(message)

        elif message.text == "Add Video":
            bussines.add_video(message)

        elif message.text == "Generate Video":
            bussines.generate_video(message)

        elif message.text == "Videos\' list":
            bussines.list_video(message)

        elif message.text == "Delete Video":
            bussines.delete_video_choise(message)

        elif (str(message.text).__contains__('https://www.youtube.com')) and bussines.Flag_Add:
                bussines.download_video(message)

        elif bussines.Flag_Generate:
            bussines.get_video(message)

        elif message.text == "add_new_admin":
            bussines.Bot.send_message(message.from_user.id, 'Send contact of new user')
            bussines.Flag_Admin = True

        elif bussines.Flag_Delete and ((re.match(r'^/[0-9]',str(message.text))) or (re.match(r'^/[0-9][0-9]',str(message.text)))):
            bussines.delete_video(message)

        elif bussines.Flag_Priority and re.match(r'^[1-5]$', message.text):
            bussines.set_prioritys(message)
        else:
            bussines.other(message)
    else:
        bussines.Bot.send_message(message.from_user.id, 'You do not have permissions')


@bussines.Bot.message_handler(content_types=['contact'])
def handle_text(message):
    if bussines.Flag_Admin:
        bussines.add_new_admin(message, message.contact.user_id)


try:
    bussines.Bot.polling(none_stop=True, interval=0)
except ConnectionError:
    print("Aborted Connection")
