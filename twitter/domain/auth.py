from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .types import URL


@dataclass
class User:
    email: str
    first_name: str
    last_name: str
    username: str
    is_active: bool = False
    is_superuser: bool = False
    password: str | None = None
    id: Optional[int] = None



@dataclass
class Profile:
    user: User
    photo: URL | None # url to photo
    background_photo: URL | None # url to profile background photo
    description: str | None
    date_joined: datetime = field(default_factory=datetime.now)


@dataclass
class Follow:
    follower_user_id: int
    followee_user_id: int
    date_created: datetime
