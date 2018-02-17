import requests
import telebot
import pytube

Bot = None
Flag = False
Panel_Flag = False
start_id = 0
finish_id = -1
html_code = ''
req = ''


def start(message):
    global Bot
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('Add Video', 'Generate Video', 'stop')
    Bot.send_message(message.from_user.id, 'Hello', reply_markup=user_markup)
    print('start')


def generate_video(message):
    global Bot
    global Flag
    Bot.send_message(message.from_user.id, "Enter your request:")
    Flag = True
    print('generated video')


def add_video(message):
    global Bot
    global Flag
    Bot.send_message(message.from_user.id, "Add link to your video:")
    Flag = True
    print('add video')


def stop(message):
    hide_markup = telebot.types.ReplyKeyboardRemove(True)
    Bot.send_message(message.from_user.id, '...', reply_markup=hide_markup)
    print('stop')


def get_video(message):
    global Bot
    global Flag
    global html_code
    global req
    global start_id
    global finish_id
    req = str(message.text)
    request = (str(message.text)).replace(' ', '+')
    url = 'https://www.youtube.com/results?search_query=' + request + '&sp=EgIYAQ%253D%253D'
    r = requests.get(url)
    html_code = str(r.text)
    i = html_code.find(
        "<li><div class=\"yt-lockup yt-lockup-tile yt-lockup-video vve-check clearfix\" data-context-item-id=")

    start_id = i + 99
    finish_id = start_id + 11

    id = html_code[start_id:finish_id]  # 2800+len 2802+len
   # print('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\''+html_code)
    print('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\''+html_code[start_id:finish_id+ 4310+(len(req)*30)])
    print('--------------------------------------------------');
    print(html_code[start_id+4041:finish_id+4041])
    g_url = 'https://www.youtube.com/watch?v=' + id

    if id == 't-face{font':
        Bot.send_message(message.from_user.id, "Video not found")
    else:
        Bot.send_message(message.from_user.id, "Generated video ->")
        Bot.send_message(message.from_user.id, g_url)
    Flag = False
    Panel_Flag = True
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('Next', 'Previous', 'Close')
    Bot.send_message(message.from_user.id, 'Next', reply_markup=user_markup)
    print('get video')


def download_video(message):
    global Flag
    Bot.send_message(message.from_user.id, "Your video has searched")
    print('downloading...')
    pytube.YouTube(message.text).streams \
        .filter(file_extension='mp4') \
        .first().download('D:\\Video\\')
    Flag = False
    Bot.send_message(message.from_user.id, "Your video is saved")
    print('...downloaded')


def other(message):
    global Bot
    global Panel_Flag
    global Flag
    global html_code
    global req
    if (message.text == 'Next') and (Panel_Flag == True):
        i = html_code.find(
            "<li><div class=\"yt-lockup yt-lockup-tile yt-lockup-video vve-check clearfix\" data-context-item-id=")
        id = html_code[i + 2800 + len(req):i + 2812 + len(req)]  # 2800+len 2812+len
        g_url = 'https://www.youtube.com/watch?v=' + id
        if id == 't-face{font':
            Bot.send_message(message.from_user.id, "Video not found")
        else:
            Bot.send_message(message.from_user.id, "Generated video ->")
            Bot.send_message(message.from_user.id, g_url)
        print('next')

    elif message.text == 'Previous':
        print('previous')

    elif message.text == 'Close':
        Panel_Flag = False
        start(message)
        print('close')
