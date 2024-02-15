from sqlalchemy.orm import Session, sessionmaker
from main import app
#test a real and genuine user registration 
def test_user_registration(client, user_data):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201
    

#test a real and genuine user login
def test_login_user(client, user_data, login_data):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200

#test a user with wrong registration details
def test_wrong_registration(client, wrong_user_data):
    response = client.post('/user/register', json=wrong_user_data)
    assert response.status_code == 422
    
#test a user with wrong login credential details
def test_wrong_login_user(client, user_data, wrong_login_data):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login', json=wrong_login_data)
    assert response.status_code == 401
