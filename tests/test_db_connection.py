import base
from sqlalchemy.sql import text

from twitter.adapters.orm import metadata
from twitter.services.unit_of_work import SqlAlchemyUnitOfWork


def test_db_connection():
    with SqlAlchemyUnitOfWork() as uow:
        uow.session.execute(text('''
            INSERT INTO users
                (email, first_name, last_name, username, password, is_active)
            VALUES (
                'nazar@gmail.com', 'Nazar', 'Annanazarov', 'n-freman', 'nazar#2003', TRUE
            );
        '''))
        assert list(uow.session.execute(text('''
            SELECT * FROM users;
        ''')))[0]
        uow.session.execute(text('''
            DELETE FROM users WHERE username = 'n-freman';
        '''))
        assert list(uow.session.execute(text('''
            SELECT * FROM users;
        '''))) == []
