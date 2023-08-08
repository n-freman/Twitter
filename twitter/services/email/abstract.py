from abc import ABC, abstractmethod


class AbstractMailService(ABC):

    @abstractmethod
    def send(self, message: str, receiver: str) -> bool:
        raise NotImplementedError
