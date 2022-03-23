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
    etf_shares_amount, etf_metal_amount = SprottScraping.get_etf_allocation(MetalEtf.PHYS)
    etf_price = Finnhub.current_price("PHYS")['c']
    metal_price = GoldApi.current_price("XAU")['price']
    print(discount_calculation(etf_shares_amount, etf_price, etf_metal_amount, metal_price))

