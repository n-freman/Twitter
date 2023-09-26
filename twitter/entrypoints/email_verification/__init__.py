from ...bootstrap import bootstrap
from ...config import (
    REDIS_EMAIL_VER_CHANNEL,
    get_redis_uri,
    get_smtp_service_credentials
)
from ...services.email.fake import FakeMailService
from ...services.email.smtp_mail_service import SMTPMailService
from ...services.email.subscriber import RedisSubscriber

bootstrap(False, False, True)


subscriber = RedisSubscriber(
    *get_redis_uri(),
    email_service=SMTPMailService(*get_smtp_service_credentials())
)
subscriber.subscribe(REDIS_EMAIL_VER_CHANNEL)
subscriber.listen()
