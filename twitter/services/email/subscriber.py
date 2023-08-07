import json

from ...adapters.pub_sub.redis_adapter import RedisAdapter
from .abstract import AbstractMailService
from .publisher import Message


class RedisSubscriber(RedisAdapter):

    def __init__(self, *args, email_service: AbstractMailService):
        super().__init__(*args)
        self._email_service = email_service

    def subscribe(self, channel: str):
        self.__subscriber = self._redis_client.pubsub()
        self.__subscriber.subscribe(channel)

    def listen(self):
        for message in self.__subscriber.listen():
            print(message, flush=True)
            if message['type'] == 'subscribe':
                continue
            try:
                message: Message = json.loads(message['data'])
            except Exception as e:
                print(e, flush=True)
                continue
            self._email_service.send(**message)
