import os
import time
import json
import urllib.request
from dotenv import load_dotenv

from attraction_parser import AttractionParser
from greeting_parser import GreetingParser
from restaurant_parser import RestaurantParser
from show_parser import ShowParser


class DynamicInfoScraper:
    def __init__(self):
        load_dotenv()
        self.attraction_url = ""
        self.restaurant_url = ""
        self.show_url = ""
        self.greeting_url = ""
        self.__init_url()
        self.name_matching = {}
        self.__load_name_matching()

    def __init_url(self):
        """
        スクレイピング用のURLを環境変数から初期化する。
        """
        self.attraction_url = os.getenv('ATTRACTION_URL')
        self.restaurant_url = os.getenv('RESTAURANT_URL')
        self.show_url = os.getenv('SHOW_URL')
        self.greeting_url = os.getenv('GREETING_URL')
        if not self.attraction_url or not self.restaurant_url or not self.show_url or not self.greeting_url:
            self.attraction_url = str(os.environ['ATTRACTION_URL'])
            self.restaurant_url = str(os.environ['RESTAURANT_URL'])
            self.show_url = str(os.environ['SHOW_URL'])
            self.greeting_url = str(os.environ['GREETING_URL'])

    def __load_name_matching(self):
        """
        disney-app とスクレイピング先の名称のマッピングファイルをロードする。

        スクレイピング先名称 -> disney-app のマッピングを返却する。
        """
        with open("./static_data/name_matching.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            self.name_matching = {value: key for key, value in data.items()}

    def __fetch_attraction_list(self):
        res = urllib.request.urlopen(self.attraction_url)
        raw_html = res.read().decode()
        return AttractionParser.parse_html(raw_html)

    def __fetch_restaurant_list(self):
        res = urllib.request.urlopen(self.restaurant_url)
        raw_html = res.read().decode()
        return RestaurantParser.parse_html(raw_html)

    def __fetch_show_list(self):
        res = urllib.request.urlopen(self.show_url)
        raw_html = res.read().decode()
        return ShowParser.parse_html(raw_html)

    def __fetch_greeting_list(self):
        res = urllib.request.urlopen(self.greeting_url)
        raw_html = res.read().decode()
        return GreetingParser.parse_html(raw_html)

    def __fetch_dynamic_info(self):
        """
        スクレイピングを実施し、スポット名称をキーにしたdictに変換する。
        返却リスト中のスポット名称はすべてスクレイピング先の表記となっている。
        """

        # スクレイピング実行
        attraction_list = self.__fetch_attraction_list()
        time.sleep(1)
        restaurant_list = self.__fetch_restaurant_list()
        time.sleep(1)
        show_list = self.__fetch_show_list()
        time.sleep(1)
        greeting_list = self.__fetch_greeting_list()

        # スポット名称をキーにしたdictの配列に変換
        all_spot_list = []
        all_spot_list.extend(attraction_list)
        all_spot_list.extend(restaurant_list)
        all_spot_list.extend(show_list)
        all_spot_list.extend(greeting_list)
        all_spot_dict = dict([(spot.name, spot.to_dict()) for spot in all_spot_list ])

        return all_spot_dict

    def fetch_dynamic_info_and_mapping_name(self):
        """
        スクレイピングを実施し、スポット名称をキーにしたdictの配列に変換する。
        また、スクレイピング先のスポット名称をdisney-appで扱うスポット名称に変換する。

        note: disney-app側に名称が存在しないスポットについては返却しない。
        """
        all_spot_dict = self.__fetch_dynamic_info()
        all_spot_replaced_name_dict = {}
        for key in all_spot_dict:
            if key not in self.name_matching:
                continue
            disney_app_name = self.name_matching[key]
            all_spot_replaced_name_dict[disney_app_name] = all_spot_dict[key]
        return all_spot_replaced_name_dict
