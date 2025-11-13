from datetime import timedelta
from app.core import auth as core_auth


def test_create_and_verify_token_roundtrip():
    token = core_auth.create_access_token({"sub": "testuser"})
    assert isinstance(token, str)

    subject = core_auth.verify_token(token)
    assert subject == "testuser"


def test_expired_token_returns_none():
    # create a token that's already expired
    token = core_auth.create_access_token({"sub": "someone"}, expires_delta=timedelta(seconds=-1))
    assert core_auth.verify_token(token) is None
