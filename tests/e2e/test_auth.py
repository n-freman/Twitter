import pytest

from tests import base
from twitter.domain import User
from twitter.services.unit_of_work import SqlAlchemyUnitOfWork


def test_registration():
    with SqlAlchemyUnitOfWork() as uow:
        initial_count = uow.session.query(User).count()
        response = base.client.post(
            '/auth/register',
            json={
                'email': 'nazar@gmail.com',
                'first_name': 'Nazar',
                'last_name': 'Ann',
                'username': 'phoenix-marko',
                'description': 'First Captain of WhiteBeard',
                'password': 'qazxsw123'
            }
        )
        assert response.status_code == 200
    with SqlAlchemyUnitOfWork() as uow:
        # Check user count increased
        assert uow.session.query(User).count() == initial_count+1


def test_login_not_activated_user():
    response = base.client.post(
        '/auth/login',
        json={
            'email': 'nazar@gmail.com',
            'password': 'qazxsw123'
        }
    )
    assert response.status_code == 400


@pytest.mark.skip(reason='Need to get otp')
def test_activate_user():
    pass


@pytest.mark.skip(reason='Need to implement prev test')
def test_login_activated_user():
    pass
