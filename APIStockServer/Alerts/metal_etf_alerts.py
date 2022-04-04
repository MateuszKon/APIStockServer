from APIStockServer.Alerts import Alerts
from APIStockServer.DataAcquisition import IPreciousMetalSpotData, IPreciousMetalEtfData, IPreciousMetalEtfInformation
from APIStockServer.Alerts.AlertSender import IAlertSender
from APIStockServer.modules.indicators_calculation import discount_calculation


class MetalEtfAlerts(Alerts):

    _METAL_CHECK_FUNCTIONS_DICTIONARY = None  # global defined later in this class
    _DISCOUNT_THRESHOLD = 10  # discount percentage to active alert

    def __init__(self,
                 etf_list: list,
                 alert_sender: IAlertSender,
                 spot_data: IPreciousMetalSpotData,
                 etf_data: IPreciousMetalEtfData,
                 etf_info: IPreciousMetalEtfInformation,
                 alert_receivers: list):
        super().__init__(alert_sender, alert_receivers)
        self.etf_list = etf_list
        self.spot_data = spot_data
        self.etf_data = etf_data
        self.etf_info = etf_info

    def current_spot_price(self, etf_name: str):
        funct = self._METAL_CHECK_FUNCTIONS_DICTIONARY[etf_name]["spot_price_function"]
        args = self._METAL_CHECK_FUNCTIONS_DICTIONARY[etf_name]["spot_price_arguments"]
        return funct(self, *args)

    def current_spot_price_gold_api(self, asset_name):
        return self.spot_data.current_spot_price(asset_name)

    def current_multiple_spot_price_gold_api(self, *assets_names):
        return [self.current_spot_price_gold_api(asset_name) for asset_name in assets_names]

    def current_etf_price(self, etf_name: str):
        asset_name = self._METAL_CHECK_FUNCTIONS_DICTIONARY[etf_name]["etf_price_argument"]
        return self.etf_data.current_etf_price(asset_name)

    def check_etf_discount(self, etf_name: str):
        etf_shares_amount, etf_metal_amount = self.etf_info.etf_allocation(etf_name)
        etf_price = self.current_etf_price(etf_name)
        metal_price = self.current_spot_price(etf_name)
        discount = discount_calculation(etf_shares_amount, etf_price, etf_metal_amount, metal_price)
        calculation_string = f"{etf_name}\n" \
                             f"Shares: {etf_shares_amount}, Etf price: {etf_price}\n" \
                             f"Metal amount: {etf_metal_amount}, Metal price: {metal_price}\n" \
                             f"Discount: {discount}\n"
        return discount, calculation_string

    def check_metal_alerts(self, print_log=False):
        for etf_name in self.etf_list:
            discount, calculation_string = self.check_etf_discount(etf_name)
            if print_log:
                print(calculation_string)
            if discount > self._DISCOUNT_THRESHOLD:
                self.send_alerts("Metal ETF Alert", calculation_string)

    _METAL_CHECK_FUNCTIONS_DICTIONARY = {"PHYS": {"spot_price_function": current_spot_price_gold_api,
                                                         "spot_price_arguments": ("XAU",),
                                                         "etf_price_argument": "PHYS"},
                                         "PLSV": {"spot_price_function": current_spot_price_gold_api,
                                                         "spot_price_arguments": ("XAG",),
                                                         "etf_price_argument": "PSLV"},
                                         "SPPP": {"spot_price_function": current_multiple_spot_price_gold_api,
                                                         "spot_price_arguments": ("XPT", "XPD",),
                                                         "etf_price_argument": "SPPP"},
                                         }


if __name__ == "__main__":
    from APIStockServer.Alerts.AlertSender import EmailSender
    from APIStockServer.DataAcquisition import GoldApi, Finnhub, MetalEtfScraping

    list_of_etfs = ["PHYS", "PLSV", "SPPP"]

    key_path = "../../data/goldapi_key"
    with open(key_path) as f_r:
        key = f_r.readline()
    gold_api = GoldApi(key)

    key_path = "../../data/finnhub_key"
    with open(key_path) as f_r:
        key = f_r.readline()
    finnhub_api = Finnhub(key)

    smtp_server = "smtp.gmail.com"
    sender_email = "mark.grengoric@gmail.com"  # Enter your address
    receiver_email = "mateusz.koniuszewski@gmail.com"  # Enter receiver address
    password = "GBvcqq7oqabLT6"
    sender = EmailSender(smtp_server, sender_email, password)

    obj = MetalEtfAlerts(list_of_etfs, sender, gold_api, finnhub_api, MetalEtfScraping(), [receiver_email, ])
    [obj.check_etf_discount(etf_name) for etf_name in list_of_etfs]


