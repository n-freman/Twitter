import pytest

pytest.skip(allow_module_level=True)

from sqlalchemy.sql import text

from twitter.adapters.orm import metadata
from twitter.services.unit_of_work import SqlAlchemyUnitOfWork


@pytest.mark.skip(reason='Need to find way to create temporary db for test')
def test_db_connection():
    with SqlAlchemyUnitOfWork() as uow:
        uow.session.execute(text('''
            INSERT INTO "users"
                (first_name, last_name, username, is_active, is_verified)
            VALUES (
                'Nazar', 'Annanazarov', 'n-freman', TRUE, TRUE
            );
        '''))
        assert list(uow.session.execute(text('''
            SELECT * FROM "users";
        ''')))[0][1:] == ('Nazar', 'Annanazarov', 'n-freman', True, True)
        uow.session.execute(text('''
            DELETE FROM "user" WHERE username = 'n-freman';
        '''))
        assert list(uow.session.execute(text('''
            SELECT * FROM "users";
        '''))) == []
