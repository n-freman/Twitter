from dotenv import load_dotenv

from .adapters import orm
from .services import unit_of_work


def bootstrap(
        start_orm: bool = True,
        create_tables: bool = True,
        load_env: bool = True,
        uow: unit_of_work.AbstractUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),
):
    if load_env:
        load_dotenv('.env')
    if start_orm:
        orm.start_mappers()
    if create_tables:
        orm.create_tables()
    return uow
