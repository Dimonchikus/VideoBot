import requests
import telebot
import pytube
import lxml.html
import os
from bot import constants

Bot = None
Flag_Generate = False
Flag_Add = False
Flag_Next = True
Flag_Panel = False
Flag_Admin = False
Flag_Priority = False
Flag_Delete = False
start_id = 0
html_code = ''


def start(message):
    global Bot
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('Add Video', 'Generate Video','Videos\' list','Delete Video','stop')
    Bot.send_message(message.from_user.id, '>>>', reply_markup=user_markup)
    print('start')


def generate_video(message):
    global Bot
    global Flag_Generate
    Bot.send_message(message.from_user.id, "Enter your request:")
    Flag_Generate = True
    print('generated video')


def add_video(message):
    global Bot
    global Flag_Add
    Bot.send_message(message.from_user.id, "Add link to your video:")
    Flag_Add = True
    print('add video')


def stop(message):
    hide_markup = telebot.types.ReplyKeyboardRemove(True)
    Bot.send_message(message.from_user.id, '...', reply_markup=hide_markup)
    print('stop')


def get_video(message):
    global Bot
    global Flag_Generate
    global Flag_Panel
    global html_code
    global start_id
    request = (str(message.text)).replace(' ', '+')
    url = 'https://www.youtube.com/results?search_query=' + request + '&sp=EgIYAQ%253D%253D'
    r = requests.get(url)

    html_code = str(r.text)
    start_id = get_id(html_code)
    id = html_code[start_id:start_id + 11]
    g_url = 'https://www.youtube.com/watch?v=' + id

    if id == 't-face{font':
        Bot.send_message(message.from_user.id, "Video not found")
    else:
        Bot.send_message(message.from_user.id, "Generated video ->")
        Bot.send_message(message.from_user.id, g_url)
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('Next', 'Close')
    Bot.send_message(message.from_user.id, 'You may get next one', reply_markup=user_markup)
    Flag_Generate = False
    Flag_Panel = True
    print('get video')


def download_video(message):
    global Flag_Add
    Bot.send_message(message.from_user.id, "Your video has searched")
    print('downloading...')
    with open('list.files', 'a', encoding='utf8') as f:
        f.write(get_name_video(message.text) + '\n' + str(message.text) + '\n')
    old_name = (get_name_video(message.text)[:-10])
    new_name = message.text[32:]
    try:
        pytube.YouTube(message.text).streams \
            .filter(file_extension='mp4') \
            .first() \
            .download('..\\Video\\')
        print('...downloaded')
    except FileExistsError:
        Bot.send_message(message.from_user.id, "This video has already been added to the list")
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('1', '2', '3', '4', '5')
    Bot.send_message(message.from_user.id, "Set the priority of the video", reply_markup=user_markup)

    Flag_Add = False


def other(message):
    global Bot
    global Flag_Panel
    global Flag_Next
    global html_code
    global start_id
    if Flag_Panel:
        if (message.text == 'Next') and Flag_Next:
            start_id += get_id(html_code[start_id:-1])
            id = html_code[start_id:start_id + 11]
            if id == 'div class=\"':
                Flag_Next = False
                Bot.send_message(message.from_user.id, 'You have reached the limit video ')
            else:
                g_url = 'https://www.youtube.com/watch?v=' + id
                Bot.send_message(message.from_user.id, g_url)
            print('next')

        elif message.text == 'Close':
            Flag_Panel = False
            Flag_Next = True
            start(message)
            print('close')
    if Flag_Add:
        print("There is no such video")
        Bot.send_message(message.from_user.id, 'There is no such video')


def get_id(html):
    id = html.find(
        "<li><div class=\"yt-lockup yt-lockup-tile yt-lockup-video vve-check clearfix\" data-context-item-id=")
    id += 99
    return id


def get_name_video(url):
    r = requests.get(url)
    html_tree = lxml.html.fromstring(r.text)
    path = ".//title"
    name_video = html_tree.xpath(path)[0]
    return str(name_video.text_content()).replace(' - YouTube','')


def user_checker(user_id):
    rez = False
    if user_id == constants.gorbenko or user_id == constants.rumsha:
        rez = True
    else:
        with open('..\\admins') as fio:
            for line in fio:
                user_id = str(user_id)
                if user_id == line.strip():
                    rez = True
    return rez


def add_new_admin(message, user_id):
    if user_checker(user_id):
        Bot.send_message(message.from_user.id, "This user is already an admin ")
    else:
        if user_id is None:
            Bot.send_message(message.from_user.id, "This user is an admin already")
            return
        with open('..\\.admins', 'a') as fos:
            fos.write(str(user_id) + "\n")
    Bot.send_message(message.from_user.id, "The contact has been added to the administrator list")
    Flag_Admin = False

def list_video(message):
    list_of_video = ''
    j = int(2)
    k = 1
    with open('list.files', 'r', encoding='utf8') as f:
         for i in f:
            if int(j) % 2 == 0:
               list_of_video += '/' + str(k) + ' ' + i.strip() + '\n'
               k += 1
            j += 1
    Bot.send_message(message.from_user.id, list_of_video)



def delete_video_choise(message):
    Bot.send_message(message.from_user.id,'Choise video for removing:')
    list_video(message)
  #  for i in list:
     #   if i[1] == message.text[1]:



def admin_checker(message):
    with open('..\\admins') as fio:
        for line in fio:
            if message.from_user.id == line.strip():
                return True
    return False

