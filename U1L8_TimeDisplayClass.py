class TimeDisplay:
    def __init__(self, display_type, seconds):
        self.display_type = display_type
        self.seconds = seconds
        self.time_string = self.display_time(display_type, seconds)

    def display_time(self, display_type:int, seconds:int):
        # parse seconds to hours, minutes, seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        # format the hours, minutes, seconds based on the display type
        if display_type == 1:
            return f"{hours}h, {minutes}m, {seconds}s"
        elif display_type == 2:
            return f"{hours}{' hour' if hours == 1 else ' hours'}\n{minutes}{' minute' if minutes == 1 else ' minutes'}\n{seconds}{' second' if seconds == 1 else ' seconds'}"
        else:
            return f"{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"

    def __str__(self):
        return self.time_string

    def __repr__(self):
        return self.time_string