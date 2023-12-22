from celery import Celery, Task

from twitter.config import (
    BROKER_HOST,
    EMAIL_SERVICE,
    get_smtp_service_credentials
)

celery_app = Celery('tasks', broker=f'pyamqp://guest@{BROKER_HOST}//')


class SendEmailTask(Task):
    name = 'send email'

    def run(self, args):
        EMAIL_SERVICE(*get_smtp_service_credentials()).send(
            args['message'],
            args['receiver']
        )


SendEmailTask = celery_app.register_task(SendEmailTask())

