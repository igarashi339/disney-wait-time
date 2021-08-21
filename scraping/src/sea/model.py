class Attraction:
    INVALID_WAIT_TIME = -1

    def __init__(self):
        self.name = ""
        self.disable_flag = False
        self.standby_pass_status = "SP情報なし"
        self.wait_time = -1

    def to_dict(self):
        ret_dict = {
            "name": self.name,
            "disable-flag": self.disable_flag,
            "standby-pass-status": self.standby_pass_status,
            "wait-time": self.wait_time
        }
        return ret_dict

