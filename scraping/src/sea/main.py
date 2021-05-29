import sys
import json
import urllib.request
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


def post_spot_info(attractions_info, restaurants_info):
    url = "https://script.google.com/macros/s/AKfycbz_B_a0lg1Ialg0Gkvq3a_8aTs9D1Di04vnVnxXPCBQl5w3yld23bxr2JbPgwLrgtbT7g/exec"
    method = "POST"
    headers = {"Content-Type": "application/json"}
    obj = {}
    for attraction in attractions_info:
        obj[attraction.name] = attraction.wait_time
    json_data = json.dumps(obj).encode("utf-8")
    request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
    urllib.request.urlopen(request)  # todo:エラーハンドリング


def main():
    name_matching = get_name_matching()
    attractions_info = fetch_realtime_attractions_info(name_matching)
    restaurants_info = fetch_realtime_restaurants_info(name_matching)
    post_spot_info(attractions_info, restaurants_info)


if __name__ == "__main__":
    main()
