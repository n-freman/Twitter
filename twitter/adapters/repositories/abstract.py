from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    @abstractmethod
    def get(self, *args):
        raise NotImplementedError

    @abstractmethod
    def add(self, *args):
        raise NotImplementedError

    @abstractmethod
    def delete(self, obj):
        raise NotImplementedError


class AbstractSQLAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session
