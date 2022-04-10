from APIStockServer.Alerts.AlertSender.Receivers import IReceivers


class ReceiversSimpleList(IReceivers):

    def __init__(self, receivers_list: list):
        self.receivers = receivers_list

    def get_receivers_list(self) -> list:
        return self.receivers
