import json

from fastapi import APIRouter, HTTPException, Response

from twitter.adapters.background_tasks import SendEmailTask
from twitter.config import SECRET_KEY
from twitter.domain.auth import Profile, User
from twitter.presentation.messages import auth as auth_messages
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
    activate_user,
    authenticate_user,
    create_jwt_token,
    get_payload,
    get_refresh_token_user,
    otp,
    register_user,
    set_user_password
)
from twitter.services.auth.exceptions import (
    OTPVerificationFail,
    UserAlreadyActive,
    UserAlreadyExists,
    UserNotFound
)
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
    uow = SqlAlchemyUnitOfWork()
    try:
        await register_user(uow, **data.as_args())
    except UserAlreadyExists:
        return Response(
            content=auth_messages.user_exists,
            status_code=400
        ) 
    SendEmailTask.delay(
        args={
            'message':otp.get_otp(data.email),
            'receiver': data.email
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
                'message': otp.get_otp(user.email),
                'receiver': user.email
            }
        )
    return {'status': 200}


@router.post('/verify-email')
async def verify_email(data: VerifyEmailSchema):
    uow = SqlAlchemyUnitOfWork()
    email = data.email
    otp = data.otp
    try:
        await activate_user(uow, email, otp)
    except UserNotFound:
        return Response(
            content=auth_messages.user_not_found,
            status_code=400
        )
    except UserAlreadyActive:
        return Response(
            content=auth_messages.user_already_active,
            status_code=400
        )
    except OTPVerificationFail:
        return Response(
            content=auth_messages.otp_verification_fail,
            status_code=400
        )
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

