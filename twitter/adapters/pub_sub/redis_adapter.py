import redis


class RedisAdapter:

    def __init__(self, host: str, port: int, decode_responses: bool = True):
        self._redis_client = redis.Redis(
            host=host,
            port=port,
            decode_responses=decode_responses
        )
