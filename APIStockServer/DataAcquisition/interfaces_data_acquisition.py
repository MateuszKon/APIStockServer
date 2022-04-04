from abc import ABC, abstractmethod


class IPreciousMetalSpotData(ABC):

    @abstractmethod
    def current_spot_price(self, asset_name: str) -> float:
        pass


class IPreciousMetalEtfData(ABC):

    @abstractmethod
    def current_etf_price(self, asset_name: str) -> float:
        pass


class IPreciousMetalEtfInformation(ABC):

    @abstractmethod
    def etf_allocation(self, etf_name: str) -> tuple:
        """
        get info about amount of shares in etf and amount of precious metals holding by this etf
        :param etf_name: get info about specified etf by this parameter
        :return: Tuple of etf shares amount and total weight of metal holding. If selected etf has multiple precious
        metals in holding (e.g. SPPP), then second element of the tuple is a list of weights'
        """
        pass
