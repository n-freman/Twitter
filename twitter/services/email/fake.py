from .abstract import AbstractMailService


class FakeMailService(AbstractMailService):

    def __init__(self, *args, **kwargs):
        pass

    def send(self, *args) -> bool:
        # print(f'Receiver: {receiver}')
        # print(f'Message: {message}')
        print(args)
        return True
