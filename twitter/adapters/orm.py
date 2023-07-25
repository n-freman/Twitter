from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, MetaData,
                        String, Table, Text, Interval)
from sqlalchemy.orm import registry, relationship
from .. import domain

metadata = MetaData()
mapper = registry()

user_table = Table(
    "user",
    metadata,
    Column("id", Integer, autoincrement=True, primary_key=True),
    Column("first_name", String(120)),
    Column("last_name", String(120)),
    Column("username", String(120)),
    Column("is_active", Boolean),
    Column("is_verified", Boolean)
)

profile_table = Table(
    "profile",
    metadata,
    Column("photo", Text),
    Column("background_photo", Text),
    Column("description", Text),
    Column("date_joined", DateTime),
    Column("user_id", ForeignKey("user.id"), primary_key=True)
)

follow_table = Table(
    "follow",
    metadata,
    Column("follower_user_id", ForeignKey("user.id"), primary_key=True),
    Column("followee_user_id", ForeignKey("user.id"), primary_key=True),
    Column("date_created", DateTime)
)

tweet_table = Table(
    "tweet",
    metadata,
    Column("id", Integer, autoincrement=True, primary_key=True),
    Column("user_id", ForeignKey("user.id")),
    Column("content", String(240)),
    Column("date_created", DateTime),
    Column("date_edited", DateTime),
    Column("quote_of", ForeignKey("tweet.id")),
    Column("reply_to", ForeignKey("tweet.id")),
    Column("previous_on_thread", ForeignKey("tweet.id"))
)

media_table = Table(
    "media",
    metadata,
    Column("id", Integer, autoincrement=True, primary_key=True),
    Column("tweet_id", ForeignKey("tweet.id")),
    Column("file_path", String(120))
)

like_table = Table(
    "like",
    metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("tweet_id", ForeignKey("tweet.id"), primary_key=True),
    Column("date_created", DateTime)
)

poll_table = Table(
    "poll",
    metadata,
    Column("tweet_id", ForeignKey("tweet.id"), primary_key=True),
    Column("length", Interval)
)

choice_table = Table(
    "choice",
    metadata,
    Column("poll_id", ForeignKey("poll.tweet_id"), primary_key=True),
    Column("number", Integer, primary_key=True),
    Column("content", String(120)),
)

answer_table = Table(
    "answer",
    metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("poll_id", ForeignKey("poll.tweet_id"), primary_key=True),
    Column("choice_number", ForeignKey("choice.number"), primary_key=True),
    Column("date_created", DateTime)
)


def start_mappers():
    mapper.map_imperatively(domain.User, user_table)
    mapper.map_imperatively(domain.Profile, profile_table)
    mapper.map_imperatively(domain.Follow, follow_table)
    mapper.map_imperatively(domain.Tweet, tweet_table)
    mapper.map_imperatively(domain.Media, media_table)
    mapper.map_imperatively(domain.Like, like_table)
    mapper.map_imperatively(domain.Poll, poll_table)
    mapper.map_imperatively(domain.Choice, choice_table)
    mapper.map_imperatively(domain.Answer, answer_table)
