from typing import Optional

from twitter.adapters.repositories.abstract import AbstractSQLAlchemyRepository
from twitter.domain.tweets import Tweet


class TweetRepository(AbstractSQLAlchemyRepository):

    def get(self, *args, **kwargs) -> Optional[Tweet]:
        return self.session.query(Tweet).filter(*args, **kwargs).first()
    
    def add(self, tweet: Tweet):
        self.session.add(tweet)
    
    def delete(self, tweet: Tweet):
        self.session.delete(tweet)
