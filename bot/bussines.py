import requests
import telebot
import pytube

Bot = None
Flag_Generate = False
Flag_Add = False
Flag_Next = True
Flag_Panel = False
start_id = 0
html_code = ''


def start(message):
    global Bot
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('Add Video', 'Generate Video', 'stop')
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
    pytube.YouTube(message.text).streams \
        .filter(file_extension='mp4') \
        .first().download('D:\\Video\\')
    Flag_Add = False
    Bot.send_message(message.from_user.id, "Your video is saved")
    print('...downloaded')


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
