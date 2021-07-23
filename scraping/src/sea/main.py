import sys
import json
import urllib.request
import datetime
from fetch_real_info import get_attraction_list


def get_name_matching():
    with open("./static_data/name_matching.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        return { value: key for key, value in data.items() }


def fetch_realtime_attractions_info(name_matching):
    ''' アトラクションのリアルタイム情報を取得する '''
    attraction_list = get_attraction_list()
    if not attraction_list:
        sys.exit(1)
    # disney-app に存在するスポットでフィルタをかける
    attraction_list_filtered = []
    for attraction in attraction_list:
        if name_matching.get(attraction.name):
            attraction.name = name_matching[attraction.name]
            attraction_list_filtered.append(attraction)
    return attraction_list_filtered


def fetch_realtime_restaurants_info(name_matching):
    # todo: 実装
    pass


def is_night_time():
    """
    ディズニーパークの閉演時間中(22:00～翌7:00)かどうか判定する。
    """
    # UTC+9h(日本時刻）を取得
    dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    hour = dt_now.hour
    print(hour)
    if hour < 7 or 22 < hour:
        return True
    return False

def post_spot_info(attractions_info, restaurants_info):
    url = "https://script.google.com/macros/s/AKfycbzMWNM6QB2lgqFGcsyWHHvTinbNitmh2OmEPaXce8j8z6ufFf8mzojztc1nnj4nooF1jA/exec"
    method = "POST"
    headers = {"Content-Type": "application/json"}
    obj = {}
    for attraction in attractions_info:
        enable_str = "中止" if attraction.disable_flag == 1 else "運営中"
        obj[attraction.name] = enable_str + "," + \
                               attraction.standby_pass_status + "," + \
                               str(attraction.wait_time)
    json_data = json.dumps(obj).encode("utf-8")
    request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
    urllib.request.urlopen(request)  # todo:エラーハンドリング


def main():
    if is_night_time():
        return
    name_matching = get_name_matching()
    attractions_info = fetch_realtime_attractions_info(name_matching)
    restaurants_info = fetch_realtime_restaurants_info(name_matching)
    post_spot_info(attractions_info, restaurants_info)


if __name__ == "__main__":
    main()
