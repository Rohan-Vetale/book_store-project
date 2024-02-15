from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from main import app
from core.model import get_db, Base
from core.settings import DATABASE_DIALECT, DATABASE_DRIVER, DATABASE_PASSWORD, DATABASE_USERNAME, DEFAULT_PORT, HOST

database_url = f"{DATABASE_DIALECT}+{DATABASE_DRIVER}://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{HOST}:{DEFAULT_PORT}/test_book_store"
engine = create_engine(database_url)
session = Session(engine)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    
@pytest.fixture
def user_data():
    return {
  "user_name": "rbv123455",
  "password": "rbv123455",
  "email": "vetalerohan@gmail.com",
  "first_name": "Rohan",
  "last_name": "Vetale",
  "state": "Maha",
  "phone": "8356853446",
  "is_verified": "true",
  "super_key": "1109011"
    }

@pytest.fixture
def wrong_user_data():
    return {
  "user_name": "rbv123455",
  "password": "rbv123455",
  "email": "vetalerohan.com",
  "first_name": "rohan",
  "last_name": "1etale",
  "state": "Maha",
  "phone": "8356853446",
  "is_verified": "true",
  "super_key": "1109011"
    }    
    
@pytest.fixture
def login_data():
    return {
  "user_name": "rbv123455",
  "password": "rbv123455"
    }
    
@pytest.fixture
def wrong_login_data():
    return {
  "user_name": "rbv1234",
  "password": "rbv123455s"
    }
    
@pytest.fixture
def user2_data():
    return {
  "user_name": "rbv123456",
  "password": "rbv123456",
  "email": "vetalerohan2@gmail.com",
  "first_name": "RohanN",
  "last_name": "VetaleN",
  "state": "Maha",
  "phone": "8356853442",
  "is_verified": "true"
    }
    
@pytest.fixture
def book_details():
    return {
    "book_name": "Watchmen",
    "author" : "Alan Moore",
    "price" : "13",
    "quantity" : "12"
    }    

@pytest.fixture
def wrong_book_details():
    return {
    "book_name": "Watchmen",
    "author" : "Alan Moore",
    "price" : "abc",
    "quantity" : "12"
    } 


@pytest.fixture
def updated_book_details():
    return {
    "book_name": "Watchman",
    "author" : "Alan Moore updated",
    "price" : "130",
    "quantity" : "120"
    } 
