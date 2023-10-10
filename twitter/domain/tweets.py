from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .types import URL


@dataclass
class Tweet:
    user_id: int
    content: str
    date_created: datetime = field(default_factory=datetime.now)
    date_edited: datetime = field(default_factory=datetime.now)
    quote_of: Optional[int] = None # ID of tweet which is quoted by current tweet
    reply_to: Optional[int] = None # ID of tweet to which this one replies
    previous_on_thread: Optional[int] = None # ID of previous tweet on thread
    id: Optional[int] = None


@dataclass
class Media:
    tweet_id: int
    file_path: URL


@dataclass
class Like:
    user_id: int
    tweet_id: int
    date_created: datetime
