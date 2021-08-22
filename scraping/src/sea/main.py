import json
import urllib.request
import datetime
from db_handler import DBHandler
from dynamic_info_scraper import DynamicInfoScraper


def is_night_time():
    """
    ディズニーパークの閉演時間中(22:00～翌7:00)かどうか判定する。
    """
    # UTC+9h(日本時刻）を取得
    dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    hour = dt_now.hour
    if hour < 7 or 21 < hour:
        return True
    return False


def update_db(dynamic_info_dict):
    """
    スクレイピング結果をDBに格納する。
    """
    db_handler = DBHandler()
    db_handler.update_raw_html("sea_dynamic_data", json.dumps(dynamic_info_dict, ensure_ascii=False))
    print(json.dumps(dynamic_info_dict, ensure_ascii=False))


def main():
    # 夜間であれば何もしない
    if is_night_time():
        return
    # スクレイピング実施
    dynamic_info_scraper = DynamicInfoScraper()
    dynamic_info_dict = dynamic_info_scraper.fetch_dynamic_info_and_mapping_name()
    # DB更新
    update_db(dynamic_info_dict)


if __name__ == "__main__":
    main()
