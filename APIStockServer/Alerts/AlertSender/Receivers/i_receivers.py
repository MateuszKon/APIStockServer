from abc import ABC, abstractmethod


class IReceivers(ABC):

    @abstractmethod
    def get_receivers_list(self) -> list:
        pass
