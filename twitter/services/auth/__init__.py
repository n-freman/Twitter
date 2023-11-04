from dataclasses import asdict
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from ... import config
from ...domain.auth import User
from ...presentation.schemas import auth
from ...services.unit_of_work import SqlAlchemyUnitOfWork

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

credential_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'}
)


async def get_refresh_token_user(token: str) -> auth.UserInDBSchema:
    try:
        payload = get_payload(token, config.REFRESH_KEY)
        user = get_user(payload.get('user_email'))
        return user
    except JWTError:
        raise credential_exception


def verify_password(
    plain_password: str,
    user: auth.UserInDBSchema
) -> bool:
    return pwd_context.verify(
        plain_password,
        user.password.get_secret_value()
    )


def set_user_password(plain_password: str, user: User):
    user.password = get_password_hash(plain_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def get_user(email: str):
    with SqlAlchemyUnitOfWork() as uow:
        user = uow.users.get(User.email==email)
        if user is None:
            return None
        user = auth.UserInDBSchema(
            **asdict(user)
        )
        return user


def authenticate_user(email: str, password: str):
    auth_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='User not found or not activated',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    user = get_user(email)
    if (
        not user or 
        not user.is_active or 
        not verify_password(password, user)
    ):
        raise auth_exception
    return user


def create_jwt_token(email: str, refresh=False):
    payload = {'user_email': email}
    expire = datetime.utcnow() + timedelta(
        minutes=(
            config.REFRESH_TOKEN_EXPIRES 
            if refresh else 
            config.ACCESS_TOKEN_EXPIRES
        )
    )
    payload.update({'exp': expire})
    encoded_jwt = jwt.encode(
        payload,
        config.REFRESH_KEY if refresh else config.SECRET_KEY,
        algorithm=config.HASHING_ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> auth.UserInDBSchema:
    try:
        payload = get_payload(token, config.SECRET_KEY)
        email: str = payload.get('user_email')
        if email is None:
            raise credential_exception

    except JWTError:
        raise credential_exception

    user = get_user(email=email)
    if user is None:
        raise credential_exception

    return user


async def get_current_active_user(
    current_user: auth.UserInDBSchema = Depends(get_current_user)
) -> auth.UserInDBSchema:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_payload(token: str, secret_key: str):
    payload = jwt.decode(
        token,
        secret_key,
        algorithms=[config.HASHING_ALGORITHM],
    )
    return payload
