from abc import ABC, abstractmethod
from typing import Self

from sqlalchemy.orm import Session

from ..adapters.orm import DEFAULT_SESSION_FACTORY
from ..adapters.repositories import (
    ProfileRepository,
    TweetRepository,
    UserRepository
)


class AbstractUnitOfWork(ABC):

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    @abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session: Session = self.session_factory()
        self.users = UserRepository(session=self.session)
        self.profiles = ProfileRepository(session=self.session)
        self.tweets = TweetRepository(session=self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

