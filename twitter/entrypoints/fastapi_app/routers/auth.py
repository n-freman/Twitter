import json

from fastapi import APIRouter, HTTPException, Response

from twitter.adapters.background_tasks import SendEmailTask
from twitter.config import SECRET_KEY
from twitter.domain.auth import Profile, User
from twitter.presentation.schemas.auth import (
    JWTSchema,
    LoginSchema,
    RefreshSchema,
    ResendVerificationSchema,
    UserCreateSchema,
    UserResponseSchema,
    VerifyEmailSchema
)
from twitter.services.auth import (
    authenticate_user,
    create_jwt_token,
    get_payload,
    get_refresh_token_user,
    otp,
    set_user_password
)
from twitter.services.auth.otp import verify_otp
from twitter.services.unit_of_work import SqlAlchemyUnitOfWork

router = APIRouter(
    prefix='/auth',
    tags=['Authentification']
)

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
        uow.profiles.add(profile)
        uow.commit()
        SendEmailTask.delay(
            args={
                'message':otp.get_otp(user.email),
                'receiver': user.email
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
        SendEmailTask.delay(                             
            args={
                'message':otp.get_otp(user.email),
                'receiver': user.email
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
async def login(data: LoginSchema) -> UserResponseSchema:
    user = authenticate_user(
        email=data.email,
        password=data.password.get_secret_value()
    )
    access_token = create_jwt_token(user.email)
    refresh_token = create_jwt_token(user.email, refresh=True)
    return UserResponseSchema(
        **user.model_dump(),
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post('/refresh')
async def refresh(
    data: RefreshSchema,
):
    user = await get_refresh_token_user(data.token.get_secret_value())
    access_token = create_jwt_token(user.email)
    refresh_token = create_jwt_token(user.email, refresh=True)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


@router.post('/verify-token')
async def verify_token(data: JWTSchema):
    payload = get_payload(
        data.token.get_secret_value(),
        SECRET_KEY
    )
    if payload:
        return {'data': 'Ok'}
    return {'data': 'Bad'}

