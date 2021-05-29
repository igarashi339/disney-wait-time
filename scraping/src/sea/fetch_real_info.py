import urllib.request
from bs4 import BeautifulSoup
from model import Attraction
ENCRYPTED_URL = "ejtofzsfbm/btvnjsbj/jogp0sfbmujnf0ejtofztfb.xbju.upebz/iunm"


def url_decoder(encrypted_url):
    decoded_url = ""
    for char in encrypted_url:
        ord_char = ord(char)
        decoded_url += chr(ord_char - 1)
    return decoded_url


def fetch_html():
    url = 'https://' + url_decoder(ENCRYPTED_URL)
    res = urllib.request.urlopen(url)
    return res.read().decode()


def parse_attraction(html):
    '''
    下記の情報を詰めてかえす
    　・アトラクション名
    　・運営中か否か
    　・待ち時間
    '''
    soup = BeautifulSoup(html, "html.parser")
    realtime_class_list = soup.find_all(class_='realtime')
    attraction_list = []
    for realtime_class in realtime_class_list:
        child_list = [child for child in realtime_class.children]
        ul_ = child_list[0]
        for li_ in ul_.children:
            name = ""
            enable = False
            wait_time = Attraction.INVALID_WAIT_TIME
            if elem_desc := li_.find(class_='desc'):
                desc_list = [child for child in elem_desc.children]
                name = elem_desc.find('h4').text
                elem_str = desc_list[-1].text.split()[0]
                if '運営中' in elem_str:
                    enable = True
            if elem_time := li_.find(class_='time'):
                if enable:
                    wait_time_str = elem_time.find('p').text.strip('待ち時間').strip("分")
                    wait_time = int(wait_time_str)
            attraction_list.append(Attraction(name, enable, wait_time))
    return attraction_list


def get_attraction_list():
    try:
        html = fetch_html()
    except:
        print("error! fetch_html")
        return None
    return parse_attraction(html)

