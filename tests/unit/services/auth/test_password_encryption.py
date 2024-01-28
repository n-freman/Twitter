import pytest

from twitter.services.auth import (
    get_password_hash,
    set_user_password,
    verify_password
)


class MockUser:
    pass


@pytest.mark.skip(reason='Need to get empty object')
def test_password_verifiction_passes():
    password = 'some!logn@har4rd#pass%word'
    hash_ = get_password_hash(password)
    user = MockUser()
    user.password = hash_
    assert verify_password(password, user) is True


@pytest.mark.skip(reason='Need to implement')
def test_user_password_set():
    pass
