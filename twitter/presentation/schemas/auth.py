import re
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, FileUrl, SecretStr
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated

from twitter.presentation.schemas.base import BaseSchema


class UserSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    username: str
    password: SecretStr


class UserInDBSchema(UserSchema):
    id: int
    is_active: bool
    is_superuser: bool


class UserResponseSchema(UserSchema):
    is_superuser: bool
    access_token: str
    refresh_token: str


class ProfileSchema(BaseModel):
    description: str
    photo: FileUrl | None = None
    background_photo: FileUrl | None = None
    date_joined: datetime = Field(default_factory=datetime.now)


class UserCreateSchema(BaseSchema, UserSchema, ProfileSchema):
    pass


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    username: str | None = None


def verify_otp(value: str) -> str:
    pattern = '\d{6}'
    assert re.match(pattern, value) is not None, f'{value} is not otp'
    return value


OTP = Annotated[str, AfterValidator(verify_otp)]


class ResendVerificationSchema(BaseModel):
    email: EmailStr


class VerifyEmailSchema(BaseModel):
    email: EmailStr
    otp: OTP


class LoginSchema(BaseModel):
    email: EmailStr
    password: SecretStr


class RefreshSchema(BaseModel):
    token: SecretStr


class JWTSchema(BaseModel):
    token: SecretStr

