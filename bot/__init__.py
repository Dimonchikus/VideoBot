import telebot
import constants
import pytube

bot = telebot.TeleBot(constants.token);



@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True);
    user_markup.row('addVideo','generateVideo','stop')
    bot.send_message(message.from_user.id,'Hello',reply_markup=user_markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
      if message.text == "stop":
         hide_markup = telebot.types.ReplyKeyboardRemove(True);
         bot.send_message(message.from_user.id, '...', reply_markup=hide_markup)
      elif message.text == "addVideo":
         bot.send_message(message.from_user.id,"Add link to your video:")
      elif message.text == "generateVideo":
         bot.send_message(message.from_user.id,"Your generated video:")
      elif str(message.text).__contains__('https://www.youtube.com'):
          bot.send_message(message.from_user.id,"Your video has searched")
          pytube.YouTube(message.text).streams\
              .filter(file_extension='mp4')\
              .first().download()

bot.polling(none_stop=True, interval=0)