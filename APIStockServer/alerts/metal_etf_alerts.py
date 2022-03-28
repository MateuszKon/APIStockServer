import time
import threading

from APIStockServer.alerts.alerts import Alerts
from APIStockServer.APIRequests import Finnhub, GoldApi
from APIStockServer.modules.email_sender import EmailSender
from APIStockServer.modules.scraping import SprottScraping, MetalEtf
from APIStockServer.modules.indicators_calculation import discount_calculation


class MetalEtfAlerts(Alerts):

    _METAL_CHECK_FUNCTIONS_DICTIONARY = None  # global defined later in this class
    _DISCOUNT_THRESHOLD = 10  # discount percentage to active alert

    def __init__(self, email_sender: EmailSender, gold_api: GoldApi, finnhub_api: Finnhub, alert_reveivers):
        super().__init__(email_sender, alert_reveivers)
        self.gold_api = gold_api
        self.finnhub_api = finnhub_api

    def current_spot_price(self, etf: MetalEtf):
        funct = self._METAL_CHECK_FUNCTIONS_DICTIONARY[etf]["spot_price_function"]
        args = self._METAL_CHECK_FUNCTIONS_DICTIONARY[etf]["spot_price_arguments"]
        return funct(self, *args)

    def current_spot_price_gold_api(self, asset_name):
        return self.gold_api.current_price(asset_name)

    def current_multiple_spot_price_gold_api(self, *assets_names):
        return [self.current_spot_price_gold_api(asset_name) for asset_name in assets_names]

    def current_etf_price(self, etf: MetalEtf):
        asset_name = self._METAL_CHECK_FUNCTIONS_DICTIONARY[etf]["etf_price_argument"]
        return self.finnhub_api.current_price(asset_name)

    def check_etf_discount(self, etf: MetalEtf):
        etf_shares_amount, etf_metal_amount = SprottScraping.get_etf_allocation(etf)
        etf_price = self.current_etf_price(etf)
        metal_price = self.current_spot_price(etf)
        discount = discount_calculation(etf_shares_amount, etf_price, etf_metal_amount, metal_price)
        calculation_string = f"{etf}\n" \
                             f"Shares: {etf_shares_amount}, Etf price: {etf_price}\n" \
                             f"Metal amount: {etf_metal_amount}, Metal price: {metal_price}\n" \
                             f"Discount: {discount}\n"
        return discount, calculation_string

    def check_metal_alerts(self, print_log=False):
        for etf in MetalEtf:
            discount, calculation_string = self.check_etf_discount(etf)
            if print_log:
                print(calculation_string)
            if discount > self._DISCOUNT_THRESHOLD:
                self.send_alerts(calculation_string)


    def start_periodic_thread(self, funct_calculate, period, *args, **kwargs):
        threading.Thread(target=funct_calculate, args=(period, *args), kwargs=kwargs, daemon=True).start()

    _METAL_CHECK_FUNCTIONS_DICTIONARY = {MetalEtf.PHYS: {"spot_price_function": current_spot_price_gold_api,
                                                         "spot_price_arguments": ("XAU",),
                                                         "etf_price_argument": "PHYS"},
                                         MetalEtf.PLSV: {"spot_price_function": current_spot_price_gold_api,
                                                         "spot_price_arguments": ("XAG",),
                                                         "etf_price_argument": "PSLV"},
                                         MetalEtf.SPPP: {"spot_price_function": current_multiple_spot_price_gold_api,
                                                         "spot_price_arguments": ("XPT", "XPD",),
                                                         "etf_price_argument": "SPPP"},
                                         }


if __name__ == "__main__":
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

    obj = MetalEtfAlerts(sender, gold_api, finnhub_api)
    [obj.check_etf_discount(etf) for etf in MetalEtf]

    # etf_shares_amount, etf_metal_amount = SprottScraping.get_etf_allocation(MetalEtf.PHYS)
    # etf_price = finnhub_api.current_price("PHYS")
    # metal_price = gold_api.current_price("XAU")
    # print(discount_calculation(etf_shares_amount, etf_price, etf_metal_amount, metal_price))

