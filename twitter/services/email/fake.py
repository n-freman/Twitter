from .abstract import AbstractMailService


class FakeMailService(AbstractMailService):

    def send(self, message: str, receiver: str) -> bool:
        print(f'Receiver: {receiver}')
        print(f'Message: {message}')
        return True
