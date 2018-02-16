import requests
import telebot
import pytube
import bs4

Bot = None
Flag = False



def get_video(message):
    global Flag
    request = (str(message.text)).replace(' ', '+')
    url = 'https://www.youtube.com/results?search_query=' + request + '&sp=EgIYAQ%253D%253D'
    r = requests.get(url)
    con = str(r.text)    #content.decode('utf8')
    i=con.find("<li><div class=\"yt-lockup yt-lockup-tile yt-lockup-video vve-check clearfix\" data-context-item-id=")

    url1 = print(con[i+99:i+110])
    # b = bs4.BeautifulSoup(con, "html.parser")
    # print(b.find('h3', {'class': 'title-and-badge style-scope ytd-video-renderer'}))
    # Bot.send_message(message.from_user.id, "Generated video ->")
    Flag = False


def download_video(message):
    global Flag
    Bot.send_message(message.from_user.id, "Your video has searched")
    pytube.YouTube(message.text).streams \
        .filter(file_extension='mp4') \
        .first().download('D:\\Video\\')
    Flag = False


def generate_video():
    global Flag
    Flag = True


def add_video(message):
    global Flag
    Bot.send_message(message.from_user.id, "Add link to your video:")
    Flag = True


def stop(message):
    hide_markup = telebot.types.ReplyKeyboardRemove(True)
    Bot.send_message(message.from_user.id, '...', reply_markup=hide_markup)
