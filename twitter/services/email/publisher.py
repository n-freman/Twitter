import json
from abc import ABC, abstractmethod
from typing import TypedDict

from ...adapters.pub_sub.redis_adapter import RedisAdapter

Message = TypedDict('Message', {'message': str,'receiver': str})


class AbstractPublisher(ABC):

    @abstractmethod
    def publish(self, channel: str, message):
        raise NotImplementedError



class RedisPublisher(AbstractPublisher, RedisAdapter):

    def publish(self, channel: str, message: Message):
        print('Publishing: ', message)
        self._redis_client.publish(channel, json.dumps(message))
