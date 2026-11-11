import pytest
from pydantic import ValidationError
from app.security import hash_password, verify_password, create_access_token, decode_access_token
from app.schemas.user import UserCreate

def test_password_hashing():
    raw = "SecurePassword123!"
    hashed = hash_password(raw)
    assert hashed != raw
    assert verify_password(raw, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_jwt_token_flow():
    payload = {"sub": "test-uuid", "username": "alice"}
    token = create_access_token(payload)
    decoded = decode_access_token(token)
    assert decoded["username"] == "alice"
    assert decoded["sub"] == "test-uuid"

def test_pydantic_schema_validations():
    valid = UserCreate(username="validuser", email="test@example.com", password="password123")
    assert valid.username == "validuser"
    assert valid.email == "test@example.com"

    with pytest.raises(ValidationError):
        UserCreate(username="ab", email="not-an-email", password="123")
