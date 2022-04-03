from abc import ABC, abstractmethod


class IPreciousMetalSpotData(ABC):

    @abstractmethod
    def current_spot_price(self, asset_name: str) -> float:
        pass


class IPreciousMetalEtfData(ABC):

    @abstractmethod
    def current_etf_price(self, asset_name: str) -> float:
        pass
