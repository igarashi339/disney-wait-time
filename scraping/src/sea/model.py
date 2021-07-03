class Attraction:
    INVALID_WAIT_TIME = -1

    def __init__(self):
        self.name = ""
        self.disable_flag = False
        self.standby_pass_status = "SP情報なし"
        self.wait_time = -1

