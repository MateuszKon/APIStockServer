from abc import ABC, abstractmethod


class IMetalEtfCalculation(ABC):

    @abstractmethod
    def handled_etf(self) -> str:
        pass

    @abstractmethod
    def calculate_etf_discount(self) -> float:
        pass

    @abstractmethod
    def etf_discount_w_string(self) -> (float, str):
        pass
