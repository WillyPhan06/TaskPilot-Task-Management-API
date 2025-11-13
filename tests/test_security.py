from app.core import security


def test_hash_and_verify_password():
    plain = "myS3cretP@ss"
    hashed = security.hash_password(plain)
    assert isinstance(hashed, str) and len(hashed) > 0
    assert security.verify_password(plain, hashed) is True
    assert security.verify_password("wrongpass", hashed) is False
