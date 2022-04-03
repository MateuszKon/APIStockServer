from APIStockServer.modules.email_sender import EmailSender


class Alerts:

    def __init__(self, email_sender: EmailSender, alert_receivers):
        self.email = email_sender
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
