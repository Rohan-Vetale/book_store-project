
from main import app

#adding a genuine book
def test_add_book(client, book_details, user_data, login_data):
    #register a user 
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201
    #login the user
    response = client.post('/user/login', json=login_data)
    #get the token 
    header_token = response.json()['access_token']
    header = {'authorization': header_token}
    #add a book
    response = client.post('book/add_book', json=book_details, headers=header)
    assert response.status_code == 201
    
#adding a wrong book
def test_add_wrong_book(client, user_data, login_data, wrong_book_details):
    #register a user 
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201
    #login the user
    response = client.post('/user/login', json=login_data)
    #get the token 
    header_token = response.json()['access_token']
    header = {'authorization': header_token}
    #add a book
    response = client.post('book/add_book', json=wrong_book_details, headers=header)
    assert response.status_code == 422
    
#get all books
def test_get_all_books(client, user_data, login_data, book_details):
    #register a user 
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201
    #login the user
    response = client.post('/user/login', json=login_data)
    #get the token 
    header_token = response.json()['access_token']
    header = {'authorization': header_token}
    #add a book
    response = client.post('book/add_book', json=book_details, headers=header)
    assert response.status_code == 201
    
    #get all books
    response = client.get('book/get_all_books', headers=header)
    assert response.status_code == 200

#get a specific book
def test_get_book(client, user_data, login_data, book_details):
    #register a user 
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201
    #login the user
    response = client.post('/user/login', json=login_data)
    #get the token 
    header_token = response.json()['access_token']
    header = {'authorization': header_token}
    #add a book
    response = client.post('book/add_book', json=book_details, headers=header)
    assert response.status_code == 201
    
    #get book with id 1
    response = client.get('book/get_book/1', headers=header)
    assert response.status_code == 200
    
#update a specific book
def test_update_book(client, user_data, login_data, book_details, updated_book_details):
    #register a user 
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201
    #login the user
    response = client.post('/user/login', json=login_data)
    #get the token 
    header_token = response.json()['access_token']
    header = {'authorization': header_token}
    #add a book
    response = client.post('book/add_book', json=book_details, headers=header)
    assert response.status_code == 201
    
    #update book with id 1
    response = client.put('book/update_book/1',json=updated_book_details , headers=header)
    assert response.status_code == 200
    
#update a specific book with wrong book id
def test_wrong_update_book(client, user_data, login_data, book_details, updated_book_details):
    #register a user 
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201
    #login the user
    response = client.post('/user/login', json=login_data)
    #get the token 
    header_token = response.json()['access_token']
    header = {'authorization': header_token}
    #add a book
    response = client.post('book/add_book', json=book_details, headers=header)
    assert response.status_code == 201
    
    #update book with id 5
    response = client.put('book/update_book/5',json=updated_book_details , headers=header)
    assert response.status_code == 400
    
    
#delete a specific book
def test_delete_book(client, user_data, login_data, book_details, updated_book_details):
    #register a user 
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201
    #login the user
    response = client.post('/user/login', json=login_data)
    #get the token 
    header_token = response.json()['access_token']
    header = {'authorization': header_token}
    #add a book
    response = client.post('book/add_book', json=book_details, headers=header)
    assert response.status_code == 201
    
    #delete book with id 1
    response = client.delete('book/delete_book/1' , headers=header)
    assert response.status_code == 200
    
#delete a specific book with wrong book id
def test_delete_wrong_book(client, user_data, login_data, book_details, updated_book_details):
    #register a user 
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201
    #login the user
    response = client.post('/user/login', json=login_data)
    #get the token 
    header_token = response.json()['access_token']
    header = {'authorization': header_token}
    #add a book
    response = client.post('book/add_book', json=book_details, headers=header)
    assert response.status_code == 201
    
    #delete book with id 5
    response = client.delete('book/delete_book/5' , headers=header)
    assert response.status_code == 400
    
#delete all books 
def test_delete_all_books(client, user_data, login_data, book_details, updated_book_details):
    #register a user 
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201
    #login the user
    response = client.post('/user/login', json=login_data)
    #get the token 
    header_token = response.json()['access_token']
    header = {'authorization': header_token}
    #add a book
    response = client.post('book/add_book', json=book_details, headers=header)
    assert response.status_code == 201
    
    #delete all books
    response = client.delete('book/delete_all_books/' , headers=header)
    assert response.status_code == 200