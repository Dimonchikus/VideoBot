import telebot
from bot import bussines
from bot import constants

bussines.Bot = telebot.TeleBot(constants.token)


@bussines.Bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('addVideo', 'generateVideo', 'stop')
    bussines.Bot.send_message(message.from_user.id, 'Hello', reply_markup=user_markup)


@bussines.Bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "stop":
        bussines.stop(message)

    elif message.text == "addVideo":
        bussines.add_video(message)

    elif message.text == "generateVideo":
        bussines.generate_video(message)


    elif (str(message.text).__contains__('https://www.youtube.com')) and bussines.Flag:
        bussines.download_video(message)

    elif bussines.Flag:
        bussines.get_video(message)


bussines.Bot.polling(none_stop=True, interval=0)
