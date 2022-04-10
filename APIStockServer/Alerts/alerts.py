from APIStockServer.Alerts.AlertSender import IAlertSender
from APIStockServer.Alerts.AlertSender.Receivers import IReceivers


class Alerts:

    def __init__(self,
                 sender: IAlertSender,
                 receivers: IReceivers):
        self.sender = sender
        self.receivers = receivers

    def get_alert_receivers(self):
        return self.receivers.get_receivers_list()

    def send_alerts(self, alert_title, alert_string):
        for receiver in self.get_alert_receivers():
            self.sender.send(receiver, alert_title, alert_string)
