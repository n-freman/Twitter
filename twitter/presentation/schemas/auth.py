from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, FileUrl, SecretStr


class UserSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    username: str
    password: SecretStr


class UserInDBSchema(UserSchema):
    is_active: bool
    is_superuser: bool


class ProfileSchema(BaseModel):
    description: str
    photo: FileUrl | None = None
    background_photo: FileUrl | None = None
    date_joined: datetime = Field(default_factory=datetime.now)


class UserCreateSchema(UserSchema, ProfileSchema):
    pass


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    username: str | None = None
