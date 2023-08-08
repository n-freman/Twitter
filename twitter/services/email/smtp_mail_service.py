import ssl
from smtplib import SMTP

from tenacity import retry, stop_after_attempt

from .abstract import AbstractMailService


class SMTPMailService(AbstractMailService):

    def __init__(self,
        host: str,
        port: int,
        password: str,
        sender: str
    ):
        self.host = host
        self.port = port
        self.password = password
        self.sender = sender

    @retry(stop=stop_after_attempt(10))
    def send(self, message: str, receiver: str) -> bool:
        context = ssl.create_default_context()
        with SMTP(self.host, self.port) as smtp_server:
            smtp_server.starttls(context=context)
            smtp_server.login(self.sender, self.password)
            smtp_server.sendmail(self.sender, [receiver], message)

    def __str__(self):
        return f'MailService({self.host}, {self.port}, {self.password}, {self.sender})'
