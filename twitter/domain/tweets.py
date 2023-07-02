from dataclasses import dataclass
from datetime import datetime

from .types import URL


@dataclass
class Tweet:
    id: int
    user_id: int
    content: str
    date_created: datetime
    date_edited: datetime
    quote_of: int | None = None # ID of tweet which is quoted by current tweet
    reply_to: int | None = None # ID of tweet to which this one replies
    previous_on_thread: int | None = None # ID of previous tweet on thread


@dataclass
class Media:
    tweet_id: int
    file_path: URL


@dataclass
class Like:
    user_id: int
    tweet_id: int
    date_created: datetime
