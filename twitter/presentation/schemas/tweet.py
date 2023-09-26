from typing import Optional

from pydantic import BaseModel


class CreateTweetSchema(BaseModel):
    content: str
    quote_of: Optional[int]
    reply_to: Optional[int]
    previous_on_threa: Optional[int]


class DeleteTweetSchema(BaseModel):
    tweet_id: int


class UpdateTweetSchema(CreateTweetSchema):
    tweet_id: int
