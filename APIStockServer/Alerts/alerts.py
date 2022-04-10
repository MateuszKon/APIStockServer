from APIStockServer.Alerts.AlertSender import IAlertSender


class Alerts:

    def __init__(self,
                 sender: IAlertSender,
                 receivers: list):
        self.sender = sender
        self.alert_receivers = receivers

    def get_alert_receivers(self):
        """
        Function will be modified, receivers will be read from SQL Database
        :return:
        """
        return self.alert_receivers

    def send_alerts(self, alert_title, alert_string):
        for receiver in self.get_alert_receivers():
            self.sender.send(receiver, alert_title, alert_string)
