class Attraction:
    INVALID_WAIT_TIME = -1

    def __init__(self, name, enable, wait_time):
        self.name = name
        self.enable = enable
        self.wait_time = wait_time

