from dataclasses import dataclass
from datetime import datetime

from .types import URL


@dataclass
class User:
    id: int
    first_name: str
    last_name: str
    username: str
    is_active: bool
    is_verified: bool


@dataclass
class Profile:
    user_id: int
    photo: URL # url to photo
    background_photo: URL # url to profile background photo
    description: str
    date_joined: datetime


@dataclass
class Follow:
    follower_user_id: int
    followee_user_id: int
    date_created: datetime
