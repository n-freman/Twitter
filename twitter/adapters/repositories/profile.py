from ...domain.auth import Profile
from .abstract import AbstractSQLAlchemyRepository


class ProfileRepository(AbstractSQLAlchemyRepository):

    def get(self, **kwargs):
        self.session.query.get(Profile).filter_by(**kwargs).first()

    def add(self, profile: Profile):
        self.session.add(profile)

    def delete(self, profile: Profile):
        pass
