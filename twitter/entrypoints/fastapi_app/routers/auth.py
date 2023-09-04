import json

from fastapi import APIRouter, Response

from ....config import REDIS_EMAIL_VER_CHANNEL, get_redis_uri
from ....domain.auth import Profile, User
from ....presentation.schemas.auth import (LoginSchema, UserCreateSchema,
                                           VerifyEmailSchema)
from ....services.auth import otp
from ....services.email.publisher import RedisPublisher
from ....services.unit_of_work import SqlAlchemyUnitOfWork

router = APIRouter(
    prefix='/auth',
    tags=['Authentification']
)
redis_publisher = RedisPublisher(*get_redis_uri())


@router.post('/register')
async def register(data: UserCreateSchema):
    '''
    Route for registering new users
    '''
    with SqlAlchemyUnitOfWork() as uow:
        user = uow.users.get(
            (User.email == data.email) \
            | (User.username == data.username)
        )
        if user is not None:
            return Response(
                content=json.dumps({
                    'detail': [
                        {
                            "type":  "user_exists",
                            "loc": [
                                'body',
                                'username',
                                'email'
                            ],
                            'msg': ("User with such"
                                "username or email already exists")
                        }
                    ]
                }),
                status_code=400
            )
        user = User(
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name,
            username=data.username
        )
        profile = Profile(
            user=user,
            photo=data.photo,
            background_photo=data.background_photo,
            description=data.description,
        )
        user.set_password(data.password)
        uow.users.add(user)
        uow.profile.add(profile)
        uow.commit()
        print(REDIS_EMAIL_VER_CHANNEL)
        redis_publisher.publish(
            REDIS_EMAIL_VER_CHANNEL,
            {
                "message": otp.get_otp(user.email),
                "receiver": user.email
            }
        )
    return {'status': 200}


@router.post('/verify-email')
async def register(data: VerifyEmailSchema):
    with SqlAlchemyUnitOfWork() as uow:
        user = uow.users.get(User.email == data.email)
        if user is None:
            return Response(
                content=json.dumps({
                    'detail': [
                        {
                            "type":  "user_doesnt_exist",
                            "loc": ['email'],
                            'msg': ("User with such"
                                " email doesn't exist")
                        }
                    ]
                }),
                status_code=400
            )
        if user.is_active:
            return Response(
                content=json.dumps({
                    'detail': [
                        {
                            "type":  "user_active",
                            "loc": ['email'],
                            'msg': ("User with such"
                                " email was already activated")
                        }
                    ]
                }),
                status_code=400
            )
        user.is_active = True
        uow.users.add(user)
        uow.commit()
    return {'detail': 'Successfully activated'}


@router.post('/login')
async def login(data: LoginSchema):
    with SqlAlchemyUnitOfWork() as uow:
        user = uow.users.get(User.email == data.email)
        if user is None:
            return Response(
                content=json.dumps({
                    'detail': [
                        {
                            "type":  "user_doesnt_exist",
                            "loc": ['email'],
                            'msg': ("User with such"
                                " email doesn't exist")
                        }
                    ]
                }),
                status_code=400
            )
        