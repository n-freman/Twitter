from .abstract import AbstractMailService


class FakeMailService(AbstractMailService):

    def __init__(self, *args, **kwargs):
        pass

    def send(self, message: str, receiver: str) -> bool:
        print(f'Receiver: {receiver}')
        print(f'Message: {message}')
        return True
