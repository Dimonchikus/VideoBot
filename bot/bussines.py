import requests
import telebot
import pytube
from selenium import webdriver

Bot = None
Flag = False


def get_video(message):
    global Flag
    request = (str(message.text)).replace(' ', '+')
    url = 'https://www.youtube.com/results?search_query=' + request + '&sp=EgIYAQ%253D%253D'
    r = requests.get(url)
    con = (r.content).decode('utf8')
    print(con)
    Bot.send_message(message.from_user.id, "Generated video ->")
    Flag = False


def download_video(message):
    global Flag
    Bot.send_message(message.from_user.id, "Your video has searched")
    pytube.YouTube(message.text).streams \
        .filter(file_extension='mp4') \
        .first().download()
    Flag = False


def generate_video(message):
    global Flag
    Flag = True


def add_video(message):
    global Flag
    Bot.send_message(message.from_user.id, "Add link to your video:")
    Flag = True


def stop(message):
    hide_markup = telebot.types.ReplyKeyboardRemove(True)
    Bot.send_message(message.from_user.id, '...', reply_markup=hide_markup)
