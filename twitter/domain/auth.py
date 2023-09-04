from dataclasses import dataclass, field
from datetime import datetime

from .types import URL

# from ..services.auth import get_password_hash, verify_password


@dataclass
class User:
    email: str
    first_name: str
    last_name: str
    username: str
    is_active: bool = False
    is_superuser: bool = False
    password: str | None = None

    # def set_password(self, password: str) -> None:
    #     self.password = get_password_hash(password)
    
    # def verify_password(self, password):
    #     return verify_password(password, self.password)


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
