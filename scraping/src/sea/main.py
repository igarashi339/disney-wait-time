import json
import datetime
import sys
from db_handler import DBHandler
from dynamic_info_scraper import DynamicInfoScraper
from past_record_analyzer import PastRecordAnalyzer


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


def merge_dynamic_data(dynamic_info_dict, mean_wait_time_dict, business_hours_dict):
    """
    スクレイピング結果と平均待ち時間情報、スポットの営業時間をマージする。
    """
    # 平均待ち時間
    for spot_name in dynamic_info_dict:
        if "wait-time" not in dynamic_info_dict[spot_name]:
            # wait-time 情報が存在しないスポットには平均待ち時間も付与しない
            continue
        if mean_wait_time_dict.get(spot_name):
            dynamic_info_dict[spot_name]["mean-wait-time"] = mean_wait_time_dict[spot_name]
        else:
            dynamic_info_dict[spot_name]["mean-wait-time"] = -1
    # スポットの営業時間
    for spot_name in dynamic_info_dict:
        if "start-time" not in dynamic_info_dict[spot_name]:
            continue
        if "end-time" not in dynamic_info_dict[spot_name]:
            continue
        dynamic_info_dict[spot_name]["start-time"] = business_hours_dict[spot_name]["start-time"]
        dynamic_info_dict[spot_name]["end-time"] = business_hours_dict[spot_name]["end-time"]
    return dynamic_info_dict


def main():
    # スクレイピング実施
    dynamic_info_scraper = DynamicInfoScraper()
    dynamic_info_dict = dynamic_info_scraper.fetch_dynamic_info_and_mapping_name()

    # 過去1習慣の動的情報を取得
    db_handler = DBHandler()
    data_obj_list = db_handler.select_resent_dynamic_data(table_name="sea_dynamic_data", date_num=7)

    # 平均待ち時間、およびスポットの営業時間を計算してデータをマージ
    mean_wait_time_dict = PastRecordAnalyzer.calc_mean_time(data_obj_list)
    business_hours_dict = PastRecordAnalyzer.calc_business_hours_dict(dynamic_info_dict, data_obj_list)
    dynamic_info_dict = merge_dynamic_data(dynamic_info_dict, mean_wait_time_dict, business_hours_dict)

    # DB更新
    db_handler.update_dynamic_data_table("sea_dynamic_data", json.dumps(dynamic_info_dict, ensure_ascii=False))


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1 and is_night_time():
        print("夜間のため処理をスキップします。")
        sys.exit()
    main()
