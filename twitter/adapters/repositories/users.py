from ...domain.auth import User
from .abstract import AbstractSQLAlchemyRepository


class UserRepository(AbstractSQLAlchemyRepository):

    def get(self, *args, **kwargs) -> User:
        return self.session.query(User).filter(*args, **kwargs).first()

    def add(self, user: User):
        self.session.add(user)

    def delete(self, user: User):
        pass
