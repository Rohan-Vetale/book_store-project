from main import app

#adding a genuine book to cart
def test_add_cart(client, book_details, user_data, login_data, cart_details):
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
    
    response = client.post('cart/add', json=cart_details, headers=header)
    assert response.status_code == 201
   

#adding a wrong book to cart
def test_add_wrong_cart(client, book_details, user_data, login_data, wrong_cart_details):
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
    
    response = client.post('cart/add', json=wrong_cart_details, headers=header)
    assert response.status_code == 400
    
# Get cart details
def test_get_cart_details(client, book_details, user_data, login_data, cart_details):
    # Register a user
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    # Login the user
    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200
    
    # Get the token
    header_token = response.json()['access_token']
    header = {'authorization': header_token}

    # Add a book
    response = client.post('/book/add_book', json=book_details, headers=header)
    assert response.status_code == 201

    # Add a book to the cart
    response = client.post('/cart/add', json=cart_details, headers=header)
    assert response.status_code == 201

    # Get cart details
    response = client.get('/cart/get', headers=header)
    assert response.status_code == 200


# Confirm order
def test_confirm_order(client, book_details, user_data, login_data, cart_details):
    # Register a user
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    # Login the user
    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200
    
    # Get the token
    header_token = response.json()['access_token']
    header = {'authorization': header_token}

    # Add a book
    response = client.post('/book/add_book', json=book_details, headers=header)
    assert response.status_code == 201

    # Add a book to the cart
    response = client.post('/cart/add', json=cart_details, headers=header)
    assert response.status_code == 201

    # Confirm order
    response = client.get('/cart/confirm', headers=header)
    assert response.status_code == 200
    
    
# Failure case for Get cart details when the user is not logged in
def test_get_cart_details_wrong(client, user_data, book_details, cart_details):
    # Register a user
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    # Add a book
    response = client.post('/book/add_book', json=book_details)
    assert response.status_code == 403  # Expecting 403 Forbidden because user is not logged in

    # Get cart details
    response = client.get('/cart/get')
    assert response.status_code == 403  # Expecting 403 Forbidden because user is not logged in



# Failure case for Confirm order when there are no items in the cart
def test_confirm_order_wrong(client, user_data, book_details, login_data):
    # Register a user
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    # Login the user
    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200
    
    # Get the token
    header_token = response.json()['access_token']
    header = {'authorization': header_token}

    # Confirm order with empty cart
    response = client.get('/cart/confirm', headers=header)
    assert response.status_code == 400  # Expecting 400 Bad Request because cart is empty
