from APIStockServer.modules.email_sender import EmailSender


class Alerts:

    _DISCOUNT_THRESHOLD = 10  # discount percentage to active alert

    def __init__(self, email_sender: EmailSender, alert_reveivers):
        self.email = email_sender
        self.alert_receivers = alert_reveivers

    def get_alert_receivers(self):
        """
        Function will be modified, receivers will be read from SQL Database
        :return:
        """
        return self.alert_receivers

    def send_alerts(self, alert_string):
        for receiver in self.get_alert_receivers():
            self.email.send(receiver, alert_string)
