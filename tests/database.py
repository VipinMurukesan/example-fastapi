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


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_user_name}:{settings.database_password}@{settings.database_host_name}:{settings.database_port}/{settings.database_name}_test"


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