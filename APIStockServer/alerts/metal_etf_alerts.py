import time
import threading

from APIStockServer.APIRequests import Finnhub, GoldApi
from APIStockServer.modules.email_sender import EmailSender as Email
from APIStockServer.modules.scraping import SprottScraping, MetalEtf
from APIStockServer.modules.indicators_calculation import discount_calculation


class MetalEtfAlerts:

    def __init__(self, email_sender: Email):
        self.email = email_sender

    def start_periodic_thread(self, funct_calculate, period, *args, **kwargs):
        threading.Thread(target=funct_calculate, args=(period, *args), kwargs=kwargs, daemon=True).start()


if __name__ == "__main__":
    key_path = "../../data/goldapi_key"
    with open(key_path) as f_r:
        key = f_r.readline()
    gold_api = GoldApi(key)

    key_path = "../../data/finnhub_key"
    with open(key_path) as f_r:
        key = f_r.readline()
    finnhub_api = Finnhub(key)

    etf_shares_amount, etf_metal_amount = SprottScraping.get_etf_allocation(MetalEtf.PHYS)
    etf_price = finnhub_api.current_price("PHYS")
    metal_price = gold_api.current_price("XAU")
    print(discount_calculation(etf_shares_amount, etf_price, etf_metal_amount, metal_price))

