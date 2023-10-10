from typing import Optional

from pydantic import BaseModel


class TweetSchema(BaseModel):
    content: str


class CreateTweetSchema(TweetSchema):
    content: str
    quote_of: Optional[int] = None
    reply_to: Optional[int] = None
    previous_on_thread: Optional[int] = None


class UpdateTweetSchema(TweetSchema):
    pass


class TweetResponseSchema(CreateTweetSchema):
    pass
