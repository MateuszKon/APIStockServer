import datetime
import time

import schedule


class AlertsScheduler:

    def __init__(self, start_hour, stop_hour, funct, *args, **kwargs):
        self.start_hour = start_hour
        self.stop_hour = stop_hour
        self.funct = funct
        self.args = args
        self.kwargs = kwargs

        self.schedule_next_day()

    @classmethod
    def run_waiting_alert(cls):
        schedule.run_pending()

    def set_hourly_alerts(self):
        if datetime.datetime.today().weekday() < 5:  # schedule only from Monday to Friday
            # TODO: Check if self.stop_hour is lesser than self.start_hour, if so, add next day to self.stop_hour
            schedule.every().second.until(self.stop_hour).do(self.funct, *self.args, **self.kwargs)

    def schedule_next_day(self):
        schedule.every().day.at(self.start_hour).do(self.set_hourly_alerts)


if __name__ == "__main__":
    AlertsScheduler("19:08", "21:00", lambda: print("Current time: {}".format(time.time())))
    while True:
        AlertsScheduler.run_waiting_alert()
        time.sleep(1)
