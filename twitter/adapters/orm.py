from sqlalchemy import (Boolean, Column, DateTime, ForeignKey,
                        ForeignKeyConstraint, Integer, Interval, MetaData,
                        String, Table, Text, create_engine)
from sqlalchemy.orm import registry, relationship, sessionmaker

from .. import config, domain

metadata = MetaData()
mapper = registry()

user_table = Table(
    "users",
    metadata,
    Column("id", Integer, autoincrement=True, primary_key=True),
    Column("email", String(120), unique=True, nullable=False),
    Column("first_name", String(120), nullable=False),
    Column("last_name", String(120), nullable=False),
    Column("username", String(120), unique=True, nullable=False),
    Column("password", Text, nullable=False),
    Column("is_active", Boolean, default=False),
    Column("is_superuser", Boolean, default=False)
)

profile_table = Table(
    "profile",
    metadata,
    Column("photo", Text, nullable=True),
    Column("background_photo", Text, nullable=True),
    Column("description", Text, nullable=True),
    Column("date_joined", DateTime, nullable=False),
    Column(
        "user_id", ForeignKey(
            "users.id",
            ondelete='CASCADE'
        ),
        primary_key=True
    )
)

follow_table = Table(
    "follow",
    metadata,
    Column(
        "follower_user_id",
        ForeignKey(
            "users.id",
            ondelete='CASCADE'
        ),
        primary_key=True
    ),
    Column(
        "followee_user_id",
        ForeignKey(
            "users.id",
            ondelete='CASCADE'
        ),
        primary_key=True
    ),
    Column("date_created", DateTime)
)

tweet_table = Table(
    "tweet",
    metadata,
    Column("id", Integer, autoincrement=True, primary_key=True),
    Column("user_id", ForeignKey("users.id", ondelete='CASCADE')),
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
    Column("tweet_id", ForeignKey("tweet.id", ondelete='CASCADE')),
    Column("file_path", String(120))
)

like_table = Table(
    "like",
    metadata,
    Column(
        "user_id",
        ForeignKey(
            "users.id",
            ondelete='CASCADE'
        ),
        primary_key=True
    ),
    Column(
        "tweet_id",
        ForeignKey(
            "tweet.id",
            ondelete='CASCADE'
        ),
        primary_key=True
    ),
    Column("date_created", DateTime)
)

poll_table = Table(
    "poll",
    metadata,
    Column(
        "tweet_id",
        ForeignKey(
            "tweet.id",
            ondelete='CASCADE'
        ),
        primary_key=True
    ),
    Column("length", Interval)
)

choice_table = Table(
    "choice",
    metadata,
    Column(
        "poll_id",
        ForeignKey(
            "poll.tweet_id",
            ondelete='CASCADE'
        ),
        primary_key=True
    ),
    Column("number", Integer, primary_key=True),
    Column("content", String(120)),
)

answer_table = Table(
    "answer",
    metadata,
    Column("id", Integer, autoincrement=True, primary_key=True),
    Column("user_id", ForeignKey("users.id", ondelete='cascade')),
    Column("poll_id", ForeignKey("poll.tweet_id", ondelete='CASCADE'), primary_key=True),
    Column("choice_number", Integer, primary_key=True),
    Column("date_created", DateTime),
    ForeignKeyConstraint(
        ['poll_id', 'choice_number'],
        ['choice.poll_id', 'choice.number']
    )
)


def start_mappers():
    mapper.map_imperatively(domain.User, user_table)
    mapper.map_imperatively(
        domain.Profile,
        profile_table,
        properties={
            "user": relationship(domain.User)
        }
    )
    mapper.map_imperatively(domain.Follow, follow_table)
    mapper.map_imperatively(domain.Tweet, tweet_table)
    mapper.map_imperatively(domain.Media, media_table)
    mapper.map_imperatively(domain.Like, like_table)
    mapper.map_imperatively(domain.Poll, poll_table)
    mapper.map_imperatively(domain.Choice, choice_table)
    mapper.map_imperatively(domain.Answer, answer_table)


def create_tables():
    metadata.create_all(
        create_engine(
            config.get_postgres_uri(),
            isolation_level="REPEATABLE READ",
        ),
    )


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config.get_postgres_uri(),
        isolation_level="REPEATABLE READ",
    )
)
