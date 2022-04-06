from datetime import datetime, timedelta, time, date
from time import sleep

import schedule


class AlertsScheduler:

    def __init__(self, funct,  start_hour=0, start_minute=0, stop_hour=0, stop_minute=0, *args, **kwargs):
        self.start_time = {"hour": start_hour, "minute": start_minute}
        self.stop_time = {"hour": stop_hour, "minute": stop_minute}

        self._is_stop_next_day = datetime.today().replace(**self.start_time) >= datetime.today().replace(
                                                                                                    **self.stop_time)
        self.funct = funct
        self.args = args
        self.kwargs = kwargs

        # Schedule functions - today alert and next days alert
        self.set_hourly_alerts()
        self.schedule_next_day()
        # Start immediately - mostly for test purpose
        self.funct(*self.args, **self.kwargs)

    @classmethod
    def run_waiting_alert(cls):
        schedule.run_pending()

    @staticmethod
    def hour_string(time_dict: dict):
        return time(**time_dict).strftime("%H:%M")

    @staticmethod
    def current_day_hour(time_dict: dict):
        return datetime.today().replace(**time_dict).strftime("%Y-%m-%d %H:%M")

    @staticmethod
    def next_day_hour(time_dict: dict):
        tomorrow = datetime.today() + timedelta(days=1)
        return tomorrow.replace(**time_dict).strftime("%Y-%m-%d %H:%M")

    def current_stop_hour(self):
        if self._is_stop_next_day:
            return self.next_day_hour(self.stop_time)
        else:
            return self.current_day_hour(self.stop_time)

    def set_hourly_alerts(self):
        if datetime.today().weekday() < 5:  # schedule only from Monday to Friday
            schedule.every().hour.until(self.current_stop_hour()).do(self.funct, *self.args, **self.kwargs)

    def schedule_next_day(self):
        schedule.every().day.at(self.hour_string(self.start_time)).do(self.set_hourly_alerts)


if __name__ == "__main__":
    AlertsScheduler(lambda: print("Current time: {}".format(datetime.now().isoformat(timespec='minutes'))),
                    start_hour=15,
                    stop_hour=17)
    while True:
        AlertsScheduler.run_waiting_alert()
        sleep(60)
