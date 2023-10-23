from fastapi import status
from app import schemas 
import pytest
from jose import JWTError, jwt
from app.config import settings


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def test_root(client):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('message') == "Welcome to Vipin's API"

def test_create_user(client):
    response = client.post("/users",json ={"email":"test@gmail.com","password":"password123"})
    new_user = schemas.UserReturn(**response.json())
    assert response.status_code == status.HTTP_201_CREATED
    assert new_user.email == "test@gmail.com"


def test_login(client,test_user):    
    response = client.post("/login",data={"username":test_user["email"],"password":test_user["password"]})
    assert response.status_code == status.HTTP_200_OK

    new_token = schemas.Token(**response.json())
    assert new_token.token_type == "bearer"

    payload = jwt.decode(new_token.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    id: int = payload.get("user_id")
    assert id == test_user["id"]


@pytest.mark.parametrize("username,password,status_code",[("wrongemail@gmail.com","password123", 403),("test@gmail.com","wrongpassword",403),("wrongemail@gmail.com","wrongpassword",403), (None,"password123",422),("test@gmail.com",None,422)])
def test_incorrect_login(client,test_user,username,password,status_code):    
    response = client.post("/login",data={"username":username,"password":password})
    assert response.status_code == status_code








