import urllib.request
from bs4 import BeautifulSoup


def fetch_html():
    url = 'https://disneyreal.asumirai.info/realtime/disneysea-wait-today.html'
    res = urllib.request.urlopen(url)
    return res.read().decode()


def main():
    try:
        html = fetch_html()
    except:
        print("error! fetch_html")
        return
    soup = BeautifulSoup(html, "html.parser")
    realtime_class_list = soup.find_all(class_='realtime')
    target_info_list = []
    for realtime_class in realtime_class_list:
        child_list = [child for child in realtime_class.children]
        ul_ = child_list[0]
        for li_ in ul_.children:
            target_info_list.append(li_.find(class_='desc'))
    for target_info in target_info_list:
        print(target_info)


if __name__ == "__main__":
    main()