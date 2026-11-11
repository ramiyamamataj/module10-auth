import pytest
from app.models.user import User
from app.schemas.user import UserCreate

def test_user_model_and_uniqueness(db_session, faker_instance):
    username = faker_instance.user_name()
    email = faker_instance.email()
    pwd = faker_instance.password()

    u_schema = UserCreate(username=username, email=email, password=pwd)
    created = User.register(db_session, u_schema)
    assert created.id is not None
    assert created.username == username
    assert created.email == email
    assert created.password_hash != pwd

    with pytest.raises(ValueError) as exc:
        User.register(db_session, u_schema)
    assert "already registered" in str(exc.value)

def test_api_register_and_login_flow(client, faker_instance):
    uname = faker_instance.user_name()
    email = faker_instance.email()
    pwd = "SecretPassword456!"

    res = client.post("/register", json={"username": uname, "email": email, "password": pwd})
    assert res.status_code == 201
    body = res.json()
    assert body["username"] == uname
    assert "password_hash" not in body
    assert "id" in body

    login_res = client.post("/login", json={"username": uname, "email": email, "password": pwd})
    assert login_res.status_code == 200
    token_body = login_res.json()
    assert "access_token" in token_body
    assert token_body["token_type"] == "bearer"
