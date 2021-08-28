import json
import datetime
import sys
from db_handler import DBHandler
from dynamic_info_scraper import DynamicInfoScraper
from mean_time_calculator import MeanTimeCalculator


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
    db_handler.update_dynamic_data_table("sea_dynamic_data", json.dumps(dynamic_info_dict, ensure_ascii=False))


def merge_dynamic_info_and_mean_wait_time(dynamic_info_dict, mean_wait_time_dict):
    """
    スクレイピング結果と平均待ち時間情報をマージする。
    """
    for spot_name in dynamic_info_dict:
        if "wait-time" not in dynamic_info_dict[spot_name]:
            # wait-time 情報が存在しないスポットには平均待ち時間も付与しない
            continue
        if mean_wait_time_dict.get(spot_name):
            dynamic_info_dict[spot_name]["mean-wait-time"] = mean_wait_time_dict[spot_name]
        else:
            dynamic_info_dict[spot_name]["mean-wait-time"] = -1
    return dynamic_info_dict


def main():
    # スクレイピング実施
    dynamic_info_scraper = DynamicInfoScraper()
    dynamic_info_dict = dynamic_info_scraper.fetch_dynamic_info_and_mapping_name()

    # 平均待ち時間を計算してデータをマージ
    mean_wait_time_dict = MeanTimeCalculator.calc_mean_time(date_num=7)
    dynamic_info_dict_with_mean_wait_time = merge_dynamic_info_and_mean_wait_time(dynamic_info_dict, mean_wait_time_dict)

    # DB更新
    update_db(dynamic_info_dict_with_mean_wait_time)


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1 and is_night_time():
        print("夜間のため処理をスキップします。")
        sys.exit()
    main()
