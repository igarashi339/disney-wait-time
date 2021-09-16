class Attraction:
    INVALID_WAIT_TIME = -1

    def __init__(self):
        self.name = ""
        self.disable_flag = False
        self.standby_pass_status = "SP情報なし"
        self.wait_time = -1  # 待ち時間[分]
        self.status = ""
        self.start_time = ""  # 営業開始時刻
        self.end_time = ""  # 影響終了時刻

    def to_dict(self):
        ret_dict = {
            "disable-flag": self.disable_flag,
            "standby-pass-status": self.standby_pass_status,
            "wait-time": self.wait_time,
            "status": self.status,
            "start-time": self.start_time,
            "end-time": self.end_time
        }
        return ret_dict


class Restaurant:
    def __init__(self):
        self.name = ""
        self.disable_flag = False
        self.wait_time = -1  # 待ち時間
        self.status = ""
        self.start_time = ""  # 営業開始時刻
        self.end_time = ""  # 営業終了時刻

    def to_dict(self):
        ret_dict = {
            "disable-flag": self.disable_flag,
            "wait-time": self.wait_time,
            "status": self.status,
            "start-time": self.start_time,
            "end-time": self.end_time
        }
        return ret_dict


class Show:
    def __init__(self):
        self.name = ""
        self.disable_flag = False
        self.start_time_list = []
        self.next_start_time = ""

    def to_dict(self):
        ret_dict = {
            "disable-flag": self.disable_flag,
            "next-start-time": self.next_start_time,
            "start-time-list": self.start_time_list
        }
        return ret_dict


class Greeting:
    def __init__(self):
        self.name = ""
        self.disable_flag = False
        self.standby_pass_status = ""
        self.wait_time = -1
        self.status = ""
        self.start_time = ""
        self.end_time = ""

    def to_dict(self):
        ret_dict = {
            "disable-flag": self.disable_flag,
            "standby-pass-status": self.standby_pass_status,
            "wait-time": self.wait_time,
            "status": self.status,
            "start-time": self.start_time,
            "end-time": self.end_time
        }
        return ret_dict


class OpeningHours:
    def __init__(self, opening_hours_str):
        """
        「10:00 ～ 19:00」形式の文字列を受け取る。
        """
        self.name = "開園時間"
        self.open_time = opening_hours_str.split(" ～ ")[0]
        self.close_time = opening_hours_str.split(" ～ ")[1]

    def to_dict(self):
        ret_dict = {
            "name": self.name,
            "open_time": self.open_time,
            "close_time": self.close_time
        }
        return ret_dict
