import json

from fastapi import APIRouter, HTTPException, Response

from twitter.config import REDIS_EMAIL_VER_CHANNEL, get_redis_uri
from twitter.domain.auth import Profile, User
from twitter.presentation.schemas.auth import (
    LoginSchema,
    RefreshSchema,
    ResendVerificationSchema,
    UserCreateSchema,
    VerifyEmailSchema
)
from twitter.services.auth import (
    authenticate_user,
    create_jwt_token,
    get_current_user,
    otp,
    set_user_password,
    verify_refresh_token
)
from twitter.services.auth.otp import verify_otp
from twitter.services.email.publisher import RedisPublisher
from twitter.services.unit_of_work import SqlAlchemyUnitOfWork

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
        set_user_password(data.password.get_secret_value(), user)
        uow.users.add(user)
        uow.profile.add(profile)
        uow.commit()
        redis_publisher.publish(
            REDIS_EMAIL_VER_CHANNEL,
            {
                "message": otp.get_otp(user.email),
                "receiver": user.email
            }
        )
    return {'status': 200}


@router.post('/resend-email-verification')
async def resend_email_verification(data: ResendVerificationSchema):
    with SqlAlchemyUnitOfWork() as uow:
        user = uow.users.get(User.email == data.email)
        if not user:
            raise HTTPException(
                status_code=400,
                detail="User with such email not found"
            )
        if user.is_active:
            raise HTTPException(
                status_code=400,
                detail="User already activated"
            )
        redis_publisher.publish(
            REDIS_EMAIL_VER_CHANNEL,
            {
                "message": otp.get_otp(user.email),
                "receiver": user.email
            }
        )
    return {'status': 200}


@router.post('/verify-email')
async def verify_email(data: VerifyEmailSchema):
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
        if not verify_otp(data.email, data.otp):
            raise HTTPException(
                status_code=400,
                detail="OTP is not valid"
            )
        user.is_active = True
        uow.users.add(user)
        uow.commit()
    return {'detail': 'Successfully activated'}


@router.post('/login')
async def login(data: LoginSchema):
    user = authenticate_user(
        email=data.email,
        password=data.password.get_secret_value()
    )
    access_token = create_jwt_token(user.email)
    refresh_token = create_jwt_token(user.email, refresh=True)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


@router.post('/refresh')
async def refresh(
    data: RefreshSchema,
):
    user = await get_current_user(
        data.token.get_secret_value(),
        refresh=True
    )
    verify_refresh_token(data.token.get_secret_value())
    access_token = create_jwt_token(user.email)
    refresh_token = create_jwt_token(user.email, refresh=True)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
