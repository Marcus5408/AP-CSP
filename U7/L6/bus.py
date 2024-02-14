class Bus:
    def __init__(self, max_stops: int):
        self.max_stops = max_stops
        self.current_stop = 1
        self.direction = 1
        self.direction_change = {
            "1": 1,
            str(max_stops): 2
        }

    def move(self):
        self.current_stop += 1 if self.direction == 1 else -1
        try:
            self.direction = self.direction_change[str(self.current_stop)]
        except KeyError:
            pass
