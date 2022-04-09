from abc import abstractmethod

from APIStockServer.Alerts.MetalEtfCalculation import IMetalEtfCalculation
from APIStockServer.DataAcquisition import IPreciousMetalSpotData, IPreciousMetalEtfData, IPreciousMetalEtfInformation
from APIStockServer.modules.indicators_calculation import discount_calculation


class SprottEtfCalculation(IMetalEtfCalculation):

    def __init__(self,
                 spot_data: IPreciousMetalSpotData,
                 etf_data: IPreciousMetalEtfData,
                 etf_info: IPreciousMetalEtfInformation,
                 ):
        self.spot_data = spot_data
        self.etf_data = etf_data
        self.etf_info = etf_info

    @abstractmethod
    def get_metal_symbols(self) -> list:
        pass

    def get_metal_symbol(self) -> str:
        return self.get_metal_symbols()[0]

    def current_etf_allocation(self):
        return self.etf_info.etf_allocation(self.handled_etf())

    def current_etf_price(self):
        return self.etf_data.current_etf_price(self.handled_etf())

    def current_spot_price(self):
        return self.spot_data.current_spot_price(self.get_metal_symbol())

    def etf_parameters(self) -> tuple:
        """
        Generate tuple of information needed for discount calculation
        :return: (etf_shares_amount, etf_price, etf_metal_amount, metal_price)
        """
        etf_shares_amount, etf_metal_amount = self.current_etf_allocation()
        etf_price = self.current_etf_price()
        metal_price = self.current_spot_price()
        return etf_shares_amount, etf_price, etf_metal_amount, metal_price

    def calculate_etf_discount(self) -> float:
        return discount_calculation(*self.etf_parameters())

    def etf_discount_w_string(self) -> (float, str):
        etf_shares_amount, etf_price, etf_metal_amount, metal_price = self.etf_parameters()
        discount = discount_calculation(etf_shares_amount, etf_price, etf_metal_amount, metal_price)
        calculation_string = f"{self.handled_etf()}\n" \
                             f"Shares: {etf_shares_amount}, Etf price: {etf_price}\n" \
                             f"Metal amount: {etf_metal_amount}, Metal price: {metal_price}\n" \
                             f"Discount: {discount}\n"
        return discount, calculation_string
