from datetime import datetime, timedelta, time, date
import time

import schedule


class AlertsScheduler:

    def __init__(self, start_hour, stop_hour, funct, *args, **kwargs):
        self.start_hour = start_hour
        self.stop_hour = stop_hour
        self.is_stop_next_day = datetime.strptime(start_hour, "%H:%M") > datetime.strptime(stop_hour, "%H:%M")
        self.funct = funct
        self.args = args
        self.kwargs = kwargs

        self.schedule_next_day()

    @classmethod
    def run_waiting_alert(cls):
        schedule.run_pending()

    def set_hourly_alerts(self):
        if datetime.today().weekday() < 5:  # schedule only from Monday to Friday
            if self.is_stop_next_day:
                tomorrow = date.today() + timedelta(days=1)
                stop_hour = "{date} {time}".format(date=tomorrow.strftime("%Y-%m-%d"), time=self.stop_hour)
            else:
                stop_hour = self.stop_hour
            schedule.every().hour.until(stop_hour).do(self.funct, *self.args, **self.kwargs)

    def schedule_next_day(self):
        schedule.every().day.at(self.start_hour).do(self.set_hourly_alerts)


if __name__ == "__main__":
    AlertsScheduler("19:08", "21:00", lambda: print("Current time: {}".format(time.time())))
    while True:
        AlertsScheduler.run_waiting_alert()
        time.sleep(1)
