import os
from attraction_parser import AttractionParser
from greeting_parser import GreetingParser
from restaurant_parser import RestaurantParser
from show_parser import ShowParser
from dotenv import load_dotenv
import urllib.request


class DynamicInfoScraper:
    def __init__(self):
        load_dotenv()
        self.attraction_url = ""
        self.restaurant_url = ""
        self.show_url = ""
        self.greeting_url = ""
        self.__init_url()

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

    def fetch_dynamic_info(self):
        """
        スクレイピングを実施し、スポット名称をキーにしたdictの配列に変換する。
        """

        # スクレイピング実行
        #attraction_list = self.__fetch_attraction_list()
        # restaurant_list = self.__fetch_restaurant_list()
        show_list = self.__fetch_show_list()
        # greeting_list = self.__fetch_greeting_list()

        # スポット名称をキーにしたdictの配列に変換
        all_spot_list = []
        # all_spot_list.extend(attraction_list)
        # all_spot_list.extend(restaurant_list)
        all_spot_list.extend(show_list)
        # all_spot_list.extend(greeting_list)
        all_spot_dict_list = [{spot.name: spot.to_dict()} for spot in all_spot_list ]

        return all_spot_dict_list
