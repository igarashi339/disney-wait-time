import json

from db_handler import DBHandler


class MeanTimeCalculator:
    @staticmethod
    def __fetch_data_from_db(date_num):
        """
        DBから過去の待ち時間情報を取得して、文字列のリストとして返却する。
        """
        db_handler = DBHandler()
        table_name = "sea_dynamic_data"
        data_str_list = db_handler.select_resent_dynamic_data(table_name, date_num)
        return data_str_list

    @staticmethod
    def __calc_mean_wait_time_for_each_spot(data_str_list):
        """
        DBから返却された待ち時間情報をもとに、各スポットの平均待ち時間を計算する。
        """
        data_obj_list = [json.loads(data_str) for data_str in data_str_list]
        sum_wait_time_dict = {} # スポット名称 -> 待ち時間合計
        target_record_num_dict = {} # スポット名称 -> 待ち時間レコード数
        for data_obj in data_obj_list:
            for spot_name in data_obj:
                if not data_obj[spot_name].get("wait-time"):
                    # 待ち時間が存在しないスポットの場合はcontinue
                    continue
                wait_time = int(data_obj[spot_name]["wait-time"])
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

    @staticmethod
    def calc_mean_time(date_num):
        """
        日数を指定し各スポットの直近の平均待ち時間を求める。
        ただし、待ち時間が-1または0のものは平均計算対象から除外される。

        Parameter:
        ----------
        date_num : int
            何日分の平均をとるかの指定。

        Return:
        -------
        name_mean_wait_time_dict : dict
            名称 -> 平均待ち時間　の辞書。
        """
        data_str_list = MeanTimeCalculator.__fetch_data_from_db(date_num)
        return MeanTimeCalculator.__calc_mean_wait_time_for_each_spot(data_str_list)