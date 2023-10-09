import os

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'somehow_really_complicated_secret_key_with_signs_like:!@#$%^&*()-_=+'
)
REFRESH_KEY = os.environ.get(
    'REFRESH_KEY',
    'somehow_really_complicated_secret_key_with_signs_like:!@#$%^&*()-_='
)
HASHING_ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRES = 15
REFRESH_TOKEN_EXPIRES = ACCESS_TOKEN_EXPIRES * 10
REDIS_EMAIL_VER_CHANNEL = os.environ.get(
    'REDIS_EMAIL_VER_CHANNEL', 'email-verification'
)
OTP_KEY_EXPIRY_TIME = int(os.environ.get(
    'OTP_KEY_EXPIRY_TIME', 7200
))


def get_postgres_uri():
    host = os.environ.get("DB_HOST", "db")
    port = 8080 if host == "localhost" else 5432
    password = os.environ.get("DB_PASSWORD", "twitterAdmin123")
    user = os.environ.get("DB_USER",  "twitteradmin")
    db_name = os.environ.get("DB_NAME", "twitter")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_redis_uri():
    host = os.environ.get("REDIS_HOST", "redis")
    port = os.environ.get("REDIS_PORT", 6379)
    return (host, port)


def get_smtp_service_credentials():
    host: str = os.environ.get(
        "EMAIL_HOST"
    )
    port: int = os.environ.get(
        "EMAIL_PORT"
    )
    password: str = os.environ.get(
        "EMAIL_PASSWORD"
    )
    sender: str = os.environ.get(
        "EMAIL_SENDER"
    )
    return host, port, password, sender
