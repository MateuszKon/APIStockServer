from abc import ABC, abstractmethod


class AbstractMetalEtf(ABC):

    @classmethod
    @abstractmethod
    def get_etf_allocation(cls, etf_name):
        pass

    @classmethod
    @abstractmethod
    def handled_etf(cls):
        pass
