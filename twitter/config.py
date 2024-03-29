import os

from twitter.services import email

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'somehow_really_complicated_secret_key_with_signs_like:!@#$%^&*()-_=+'
)
REFRESH_KEY = os.environ.get(
    'REFRESH_KEY',
    'somehow_really_complicated_secret_key_with_signs_like:!@#$%^&*()-_'
)
HASHING_ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRES = 15
REFRESH_TOKEN_EXPIRES = ACCESS_TOKEN_EXPIRES * 10

OTP_KEY_EXPIRY_TIME = int(os.environ.get(
    'OTP_KEY_EXPIRY_TIME', 7200
))

EMAIL_SERVICE: email.AbstractMailService = email.FakeMailService # type: ignore
BROKER_HOST: str = os.environ.get('BROKER_HOST') # type: ignore

ALLOWED_ORIGINS = [
    'http://localhost:3000',
]


def get_postgres_uri():
    host = os.environ.get("DB_HOST", "db")
    port = os.environ.get("DB_PORT", 5432)
    password = os.environ.get("DB_PASSWORD", "twitterAdmin123")
    user = os.environ.get("DB_USER",  "twitteradmin")
    db_name = os.environ.get("DB_NAME", "twitter")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_redis_uri():
    host = os.environ.get("REDIS_HOST", "redis")
    port = os.environ.get("REDIS_PORT", 6379)
    return (host, port)


def get_smtp_service_credentials():
    host: str = os.environ.get("EMAIL_HOST") # type: ignore
    port: int = os.environ.get("EMAIL_PORT") # type: ignore
    password: str = os.environ.get("EMAIL_PASSWORD") # type: ignore
    sender: str = os.environ.get("EMAIL_SENDER") # type: ignore
    return host, port, password, sender

