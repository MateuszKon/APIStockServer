from APIStockServer.Alerts.AlertSender import IAlertSender


class Alerts:

    def __init__(self,
                 alert_sender: IAlertSender,
                 alert_receivers: list):
        self.email = alert_sender
        self.alert_receivers = alert_receivers

    def get_alert_receivers(self):
        """
        Function will be modified, receivers will be read from SQL Database
        :return:
        """
        return self.alert_receivers

    def send_alerts(self, alert_title, alert_string):
        for receiver in self.get_alert_receivers():
            self.email.send(receiver, alert_title, alert_string)
