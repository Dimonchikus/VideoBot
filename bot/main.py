import telebot
from bot import bot
from bot import constants

bot.Bot = telebot.TeleBot(constants.token)


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('addVideo', 'generateVideo', 'stop')
    bot.send_message(message.from_user.id, 'Hello', reply_markup=user_markup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "stop":
        bot.stop(message)

    elif message.text == "addVideo":
        bot.add_video(message)

    elif message.text == "generateVideo":
        bot.generate_video(message)


    elif (str(message.text).__contains__('https://www.youtube.com')) and bot.Flag:
        bot.download_video(message)

    elif bot.Flag:
        bot.get_video(message)


bot.polling(none_stop=True, interval=0)
