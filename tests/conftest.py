from fastapi.testclient import TestClient
from app.main import app
from fastapi import status
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from app.database import get_db
from app import models
import pytest
from app.oauth2 import create_access_token
from app import models


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_user_name}:{settings.database_password}@{settings.database_host_name}:{settings.database_port}/{settings.database_name}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)


#@pytest.fixture(scope="function") #-- default
@pytest.fixture
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
           
   

#@pytest.fixture(scope="function") #-- default
@pytest.fixture
def client(session):
    # Dependency
    def override_get_db():        
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client 


@pytest.fixture
def test_user(client):
    user_data = {"email":"test@gmail.com","password":"password1234"}
    response = client.post("/users",json =user_data)
    assert response.status_code == status.HTTP_201_CREATED
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user    

@pytest.fixture
def test_user1(client):
    user_data = {"email":"test1@gmail.com","password":"password1234"}
    response = client.post("/users",json =user_data)
    assert response.status_code == status.HTTP_201_CREATED
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user 

@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client,token):
    client.headers ={
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(session,test_user,test_user1):
    posts_data = [{
        "title" : "first title",
        "content" : "first content",
        "owner_id" : test_user['id']
    },{
        "title" : "second title",
        "content" : "second content",
        "owner_id" : test_user['id']
    },{
        "title" : "third title",
        "content" : "third content",
        "owner_id" : test_user['id']
    },
    {
        "title" : "fourth title",
        "content" : "fourth content",
        "owner_id" : test_user1['id']
    }     
    ]
    all_posts = [models.Post(**post) for post in posts_data]
    session.add_all(all_posts)
    session.commit()
    return session.query(models.Post).all()

