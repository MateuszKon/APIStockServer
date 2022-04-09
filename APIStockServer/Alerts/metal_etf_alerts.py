from typing import List

from APIStockServer.Alerts import Alerts
from APIStockServer.Alerts.AlertSender import IAlertSender
from APIStockServer.Alerts.MetalEtfCalculation import IMetalEtfCalculation


class MetalEtfAlerts(Alerts):

    def __init__(self,
                 alert_sender: IAlertSender,
                 etfs_calculators: List[IMetalEtfCalculation],
                 alert_receivers: list,
                 discount_threshold=10):
        super().__init__(alert_sender, alert_receivers)
        self.etfs_calculators = etfs_calculators
        self.__discount_threshold = discount_threshold

    @property
    def discount_threshold(self):
        """
        Discount threshold activating alert. Value between -100.0 and 100.0 - percentage value; positive number is a
        discount, negative value is a premium
        """
        return self.__discount_threshold

    @discount_threshold.setter
    def discount_threshold(self, value):
        if -100 < value < 1000:
            self.__discount_threshold = value
        else:
            raise ValueError("Discount value should be between -100.0 and 100.0")

    def check_metal_alerts(self, print_log=False):
        for etf_calculator in self.etfs_calculators:
            discount, calculation_string = etf_calculator.etf_discount_w_string()
            if print_log:
                print(calculation_string)
            if discount > self.discount_threshold:
                self.send_alerts("Metal ETF Alert", calculation_string)


if __name__ == "__main__":
    from APIStockServer.Alerts.AlertSender import EmailSender
    from APIStockServer.Alerts.MetalEtfCalculation import SprottEtfCalculation
    from APIStockServer.Alerts.MetalEtfCalculation import PhysEtfCalculation, PslvEtfCalculation, SpppEtfCalculation
    from APIStockServer.DataAcquisition import GoldApi, Finnhub, MetalEtfScraping

    key_path = "../../data/goldapi_key"
    with open(key_path) as f_r:
        key = f_r.readline()
    gold_api = GoldApi(key)

    key_path = "../../data/finnhub_key"
    with open(key_path) as f_r:
        key = f_r.readline()
    finnhub_api = Finnhub(key)

    metal_info_scraper = MetalEtfScraping()

    smtp_server = "smtp.gmail.com"
    sender_email = "mark.grengoric@gmail.com"  # Enter your address
    receiver_email = "mateusz.koniuszewski@gmail.com"  # Enter receiver address
    password = "GBvcqq7oqabLT6"
    sender = EmailSender(smtp_server, sender_email, password)

    list_of_sprott_etfs = [PhysEtfCalculation, PslvEtfCalculation, SpppEtfCalculation]
    calculators = list()
    for C in list_of_sprott_etfs:
        C: SprottEtfCalculation
        calculators.append(C(spot_data=gold_api,
                             etf_data=finnhub_api,
                             etf_info=metal_info_scraper
                             )
                           )

    obj = MetalEtfAlerts(sender, calculators, [receiver_email, ])
    obj.check_metal_alerts(print_log=True)


