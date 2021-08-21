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
    soup = BeautifulSoup(html, "html.parser")
    realtime_class_list = soup.find_all(class_='realtime')
    attraction_list = []
    for realtime_class in realtime_class_list:
        child_list = [child for child in realtime_class.children]
        ul_ = child_list[0]
        for li_ in ul_.children:
            attraction = Attraction()
            enable = False
            wait_time = Attraction.INVALID_WAIT_TIME
            if elem_desc := li_.find(class_='desc'):
                # name
                attraction.name = elem_desc.find('h4').text
                # standby pass status
                if elem_fp := elem_desc.find(class_="fp"):
                    attraction.standby_pass_status = elem_fp.text
                # disable_flag
                for child in elem_desc.children:
                    if not child:
                        continue
                    if not child.text:
                        continue
                    if "中止" in child.text:
                        attraction.disable_flag = True
            if elem_time := li_.find(class_='time'):
                wait_time_str = elem_time.find('p').text.strip('待ち時間').strip("分")
                attraction.wait_time = int(wait_time_str)
            attraction_list.append(attraction)
    return attraction_list


def get_attraction_list():
    try:
        html = fetch_html()
    except:
        print("error! fetch_html")
        return None
    return parse_attraction(html)

