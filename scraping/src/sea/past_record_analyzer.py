DATETIME_COL = 0
DATA_COL = 1


class PastRecordAnalyzer:
    @classmethod
    def tuple_to_str(cls, tuple_obj):
        return str(tuple_obj[0]) + "~" + str(tuple_obj[1])

    @classmethod
    def calc_mean_time(cls, data_obj_list):
        """
        日数を指定し各スポットの直近の平均待ち時間を求める。
        ただし、待ち時間が-1または0のものは平均計算対象から除外される。

        Parameter:
        ----------
        data_obj_list : array-like(obj)
            直近の動的データのリスト。

        Return:
        -------
        name_mean_wait_time_dict : dict
            名称 -> 平均待ち時間　の辞書。
        """
        sum_wait_time_dict = {} # スポット名称 -> 待ち時間合計
        target_record_num_dict = {} # スポット名称 -> 待ち時間レコード数
        for data_obj in data_obj_list:
            for spot_name in data_obj[DATA_COL]:
                if not data_obj[DATA_COL][spot_name].get("wait-time"):
                    # 待ち時間が存在しないスポットの場合はcontinue
                    continue
                wait_time = int(data_obj[DATA_COL][spot_name]["wait-time"])
                if wait_time == 0 or wait_time == -1:
                    # 待ち時間が不正な場合は計算対象から除外
                    continue
                if sum_wait_time_dict.get(spot_name):
                    sum_wait_time_dict[spot_name] += wait_time
                    target_record_num_dict[spot_name] += 1
                else:
                    sum_wait_time_dict[spot_name] = wait_time
                    target_record_num_dict[spot_name] = 1
        assert len(sum_wait_time_dict) == len(target_record_num_dict)
        mean_wait_time_dict = {} # スポット名称 -> 平均待ち時間
        for spot_name in sum_wait_time_dict:
            mean_wait_time_dict[spot_name] = int(sum_wait_time_dict[spot_name] / target_record_num_dict[spot_name])
        return mean_wait_time_dict

    @classmethod
    def calc_each_timespan_mean_time(cls, data_obj_list):
        """
        各タイムスパンの平均待ち時間を計算する。

        Parameter:
        ----------
        data_obj_list : array-like(obj)
            直近の動的データのリスト。

        Return:
        -------
        name_mean_wait_time_dict : dict
            名称 -> (時間帯 -> 平均待ち時間)　の辞書。
        """
        timespan_start_time = 7 # 時
        timespan_end_time = 22  # 時
        timespan_size = 1
        target_timespan_list = [(begin, begin + timespan_size) for begin in range(timespan_start_time, timespan_end_time, timespan_size)]

        # まず時間帯 -> (名称 -> 平均待ち時間)の辞書を計算する
        timespan_name_meantime_dict = {}
        for time_span in target_timespan_list:
            timespan_name_meantime_dict[cls.tuple_to_str(time_span)] = {}
            # 該当のタイムスパンの動的データのみフィルタリングする
            target_time_dynamic_data_list = []
            for data_obj in data_obj_list:
                date_time = data_obj[DATETIME_COL]
                if time_span[0] <= date_time.hour < time_span[1]:
                    target_time_dynamic_data_list.append(data_obj)
            mean_time_dict = PastRecordAnalyzer.calc_mean_time(target_time_dynamic_data_list)
            timespan_name_meantime_dict[cls.tuple_to_str(time_span)] = mean_time_dict

        # 名称 -> (時間帯 -> 平均待ち時間)の辞書に変換する
        name_timespan_meantime_dict = {}
        for time_span in target_timespan_list:
            for name in timespan_name_meantime_dict[cls.tuple_to_str(time_span)]:
                if name not in name_timespan_meantime_dict:
                    name_timespan_meantime_dict[name] = {}
                name_timespan_meantime_dict[name][cls.tuple_to_str(time_span)] = timespan_name_meantime_dict[cls.tuple_to_str(time_span)][name]
        return name_timespan_meantime_dict


    @classmethod
    def calc_business_hours_dict(cls, dynamic_info_dict, data_obj_list):
        """
        各スポットの営業時間情報を計算する。

        Return:
        -------
        下記のような辞書
        {
            "spot-name": {
                "start-time": "10:00",
                "end-time": "19:00"
            },
            ...
        }
        """
        business_hours_dict = {}
        for spot_name in dynamic_info_dict:
            # 営業時間の存在しないスポットはcontinue
            if "start-time" not in dynamic_info_dict[spot_name]:
                continue
            if "end-time" not in dynamic_info_dict[spot_name]:
                continue
            business_hours_dict[spot_name] = {
                "start-time": "",
                "end-time": ""
            }
            # 最新のスクレイピング結果に営業時間情報が載っていればそれを採用
            if dynamic_info_dict[spot_name]["start-time"] != "" and dynamic_info_dict[spot_name]["end-time"] != "":
                business_hours_dict[spot_name]["start-time"] = dynamic_info_dict[spot_name]["start-time"]
                business_hours_dict[spot_name]["end-time"] = dynamic_info_dict[spot_name]["end-time"]
                continue
            # 過去をさかのぼって不正でない営業時間を見つける
            for obj in data_obj_list:
                data_obj = obj[DATA_COL]
                if "start-time" not in data_obj[spot_name]:
                    continue
                if "end-time" not in data_obj[spot_name]:
                    continue
                if data_obj[spot_name]["start-time"] != "" and data_obj[spot_name]["end-time"] != "":
                    business_hours_dict[spot_name]["start-time"] = data_obj[spot_name]["start-time"]
                    business_hours_dict[spot_name]["end-time"] = data_obj[spot_name]["end-time"]
                    break
        return business_hours_dict