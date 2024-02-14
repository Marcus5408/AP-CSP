class Bus:
    def __init__(self, max_stops: int):
        self.max_stops = max_stops
        self.current_stop = 1
        self.direction = 1

    def move(self):
        self.current_stop += 1 if self.direction == 1 else -1
        self.direction = 1 if self.current_stop == 1 else 2 if self.current_stop == self.max_stops else 1
