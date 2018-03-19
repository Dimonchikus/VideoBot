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
Flag_Final_Removing = False
start_id = 0
html_code = ''
count_of_video = 0
deleted_video_id = ''


def start(message):
    global Bot
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('Add Video', 'Delete Video', 'stop')
    user_markup.row('Generate Video', 'Videos\' list')
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
    global count_of_video

    if count_of_video >= 20:
        Bot.send_message(message.from_user.id,
                         "If you add new video this video will delete\n" + constants.youtube + overflow()[1])
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


def delete_overflow(del_video):
    os.remove(constants.videos + str(del_video[1]) + '.mp4')
    f = open(constants.priority_list).readlines()
    f2 = open(constants.videos_list).readlines()
    f.pop(del_video[0])
    f2.pop(del_video[0] * 2)
    f2.pop((del_video[0] * 2))
    with open(constants.priority_list, 'w') as F:
        F.writelines(f)
    with open(constants.videos_list, 'w') as F:
        F.writelines(f2)


def download_video(message):
    global Flag_Add
    global Flag_Priority
    global count_of_video

    if count_of_video >= 20:
        delete_overflow(overflow())

    flag = True
    with open(constants.videos_list, 'r', encoding='utf8') as fio:
        with open(constants.videos_list, 'a', encoding='utf8') as f:
            for i in fio:
                if i.strip().__contains__(message.text):
                    flag = False
            if flag:
                f.write(get_name_video(message.text) + '\n' + str(message.text) + '\n')
            else:
                Bot.send_message(message.from_user.id, "You have already had that video")

    if flag:
        Bot.send_message(message.from_user.id, "Your video has searched\nDownloading...")

        print('downloading...')

        Flag_Add = False

        new_name = message.text[-11:]

        user_markup = telebot.types.ReplyKeyboardMarkup(True)
        user_markup.row('1', '2', '3', '4', '5')
        Bot.send_message(message.from_user.id, "Set the priority of the video", reply_markup=user_markup)

        pytube.YouTube(message.text).streams \
            .filter(file_extension='mp4') \
            .first() \
            .download(constants.videos, new_name)

        print('...downloaded')

        Bot.send_message(message.from_user.id, "This video has already been added to the list")

        with open('priority', 'a', encoding='utf8') as fio:
            fio.write(new_name + ' ')

        Flag_Priority = True
        count_of_video += 1


def overflow():
    with open(constants.priority_list) as fis:
        list_of_v = fis.readlines()
    del_video = [len(list_of_v) - 1, list_of_v[len(list_of_v) - 1].split()[0],  # [numb, video_id, priority]
                 list_of_v[len(list_of_v) - 1].split()[1]]
    for i in range(len(list_of_v))[::-1]:
        if i == 0:
            break
        if int(del_video[2]) <= int(list_of_v[i - 1].split()[1]):
            del_video = [i - 1, list_of_v[i - 1].split()[0], list_of_v[i - 1].split()[1]]
    print(del_video)
    return del_video


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
                g_url = constants.youtube + id
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
    return str(name_video.text_content()).replace(' - YouTube', '')


def user_checker(user_id):
    rez = False
    if user_id == constants.gorbenko or user_id == constants.rumsha:
        rez = True
    else:
        with open(constants.admins) as fio:
            for line in fio:
                user_id = str(user_id)
                if user_id == line.strip():
                    rez = True
    return rez


def add_new_admin(message, user_id, first_name):
    global Flag_Admin
    print(user_id, first_name)
    if user_checker(user_id):
        Bot.send_message(message.from_user.id, "This user is already an admin ")
    else:
        if user_id is None:
            Bot.send_message(message.from_user.id, "This user is not registered in Telegram")
            return
        with open(constants.admins, 'a') as fos:
            fos.write(str(user_id) + "\n")
        Bot.send_message(message.from_user.id, "The contact has been added to the administrator list")
    Flag_Admin = False


def list_video(message):
    list_of_video = ''
    j = int(2)
    k = 1
    with open(constants.videos_list, 'r', encoding='utf8') as f:
        for i in f:
            if int(j) % 2 == 0:
                list_of_video += '/' + str(k) + ' ' + i.strip() + '\n'
                k += 1
            j += 1
    Bot.send_message(message.from_user.id, list_of_video)


def delete_video_choise(message):
    Bot.send_message(message.from_user.id, 'Choise video for removing:')
    list_video(message)
    global Flag_Delete
    Flag_Delete = True


def admin_checker(message):
    with open(constants.admins) as fio:
        for line in fio:
            if message.from_user.id == line.strip():
                return True
    return False


def delete_video(message):
    global deleted_video_id
    number = int(message.text[1]) * 2
    iterator = 1
    with open(constants.videos_list, 'r', encoding='utf8') as f:
        for i in f:
            if (iterator == number):
                Bot.send_message(message.from_user.id, 'Remove this video?')
                deleted_video_id = i.strip()
                Bot.send_message(message.from_user.id, deleted_video_id)
            iterator += 1
    global Flag_Final_Removing
    Flag_Final_Removing = True
    global Flag_Delete
    Flag_Delete = False
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('Delete', 'Leave')
    Bot.send_message(message.from_user.id, "Make a choice", reply_markup=user_markup)


def final_removing(message):
    global deleted_video_id
    global count_of_video
    list_of_video = list_video(message)
    list_of_new_video = ''
    if (str(message.text) == 'Delete'):
        Bot.send_message(message.from_user.id, 'Removing')
        os.remove(constants.videos + str(deleted_video_id[-11:]) + '.mp4')
        for i in list_of_video:
            s = i.strip()
            if not ((s == get_name_video(deleted_video_id)) or (s == deleted_video_id)):
                list_of_new_video += i + '\n'
            with open(constants.videos_list, 'w', encoding='utf8') as f:
                f.write(list_of_new_video)
        Bot.send_message(message.from_user.id, 'Done')
        start(message)
    elif (str(message.text) == 'Leave'):
        start(message)
    global Flag_Final_Removing
    Flag_Final_Removing = False

    new_priority = ''

    with open(constants.priority_list) as fos:
        for line in fos:
            if line.split()[0] == deleted_video_id[-11:]:
                pass
            else:
                new_priority += line + '\n'
    with open(constants.priority_list, 'w') as fis:
        fis.write(new_priority)

    count_of_video -= 1


def set_prioritys(message):
    with open(constants.priority_list, 'a', encoding='utf8') as fio:
        fio.write(message.text + '\n')
    start(message)
