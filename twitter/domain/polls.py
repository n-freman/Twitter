from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Poll:
    tweet_id: int
    length: timedelta


@dataclass
class Choice:
    poll_id: int
    number: int
    content: str


@dataclass
class Answer:
    user_id: int
    poll_id: int
    answer_number: int
    date_created: datetime
