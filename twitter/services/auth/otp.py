import base64
from datetime import datetime

import pyotp

from ...config import OTP_KEY_EXPIRY_TIME, SECRET_KEY


def get_otp(email: str) -> str:
    key = base64.b32encode(generate_key(email).encode())
    OTP = pyotp.TOTP(key, interval=OTP_KEY_EXPIRY_TIME)
    return OTP.now()


def verify_otp(email: str, otp: str) -> bool:
    key = base64.b32encode(generate_key(email).encode())
    OTP = pyotp.TOTP(key, interval=OTP_KEY_EXPIRY_TIME)
    return OTP.verify(otp)


def generate_key(email: str) -> str:
    return f'{email}{datetime.date(datetime.now())}{SECRET_KEY}'
