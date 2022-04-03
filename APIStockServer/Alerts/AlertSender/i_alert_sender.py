from abc import ABC, abstractmethod


class IAlertSender(ABC):

    @abstractmethod
    def send(self, receiver, subject: str, message: str):
        pass
