"""
@Author: Rohan Vetale

@Date: 2024-02-13 12:40

@Last Modified by: Rohan Vetale

@Last Modified time: 2024-02-14 19:23

@Title : Book cart book module
"""

from fastapi import APIRouter, status, Response, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from core.schema import CartItemsSchema
from core.model import get_db, Cart, Books, CartItems, Users
from core.utils import send_confirmation_mail

router_cart = APIRouter()

@router_cart.post('/add', status_code=status.HTTP_201_CREATED, tags=["Cart"])
def add_book_to_cart(body: CartItemsSchema, response: Response, request: Request, db: Session = Depends(get_db)):
    """
    Description: Function used to add book to a cart
    Parameter: body: CartItemsSchema object, response : Response object, db : database session, request: User Request.
    Return: Message of a book added to cart with status code 201
    """
    try:
        cart_data = db.query(Cart).filter_by(user_id=request.state.user.id).one_or_none()
        if cart_data is None:
            cart_data = Cart(user_id=request.state.user.id,total_price=0,total_quantity=0)
            db.add(cart_data)
            db.commit()
            db.refresh(cart_data)
        book_data = db.query(Books).filter_by(id=body.book_id).one_or_none()
        if book_data is None:
            raise HTTPException(detail="This book is not present ", status_code=status.HTTP_400_BAD_REQUEST)
        if body.quantity > book_data.quantity:
            raise HTTPException(detail=f"Book exists with quantity {book_data.quantity}",
                                status_code=status.HTTP_400_BAD_REQUEST)

        total_books_price = body.quantity * book_data.price
        cart_items_data = db.query(CartItems).filter_by(book_id=body.book_id,cart_id=cart_data.id).one_or_none()
        if cart_items_data is None:
            cart_items_data = CartItems(price=total_books_price, quantity=body.quantity, book_id=book_data.id,
                                        cart_id=cart_data.id)
            db.add(cart_items_data)
        else:
            cart_data.total_price -= cart_items_data.price
            cart_data.total_quantity -= cart_items_data.quantity
            cart_items_data.quantity = body.quantity
            cart_items_data.price = total_books_price

        cart_data.total_price += total_books_price
        cart_data.total_quantity += body.quantity
        db.commit()
        db.refresh(cart_data)
        db.refresh(cart_items_data)
        return {'message': 'Book added in cart Successfully', 'status': 201}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}
    


@router_cart.get('/get', status_code=status.HTTP_200_OK, tags=["Cart"])
def get_cart_details(request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Description: Function used to get book from a cart
    Parameter:  response : Response object, db : database session, request: User Request.
    Return: Message of a cart details
    """
    try:
        cart_data = db.query(Cart).filter_by(user_id=request.state.user.id).one_or_none()
        if cart_data is None:
            raise HTTPException(detail='This cart is not present ', status_code=status.HTTP_400_BAD_REQUEST)
        if cart_data.total_quantity == 0:
            raise HTTPException(detail="The cart is empty", status_code=status.HTTP_400_BAD_REQUEST)
        card_items_data = db.query(CartItems).filter_by(cart_id=cart_data.id).all()
        return {'message': "Card Data found Successfully", 'status': 200, 'cart_data': cart_data,'cart_items':card_items_data}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}

@router_cart.get('/confirm', status_code=status.HTTP_200_OK, tags=["Cart"])
def confirm_order(response: Response, request: Request, db: Session = Depends(get_db)):
    """
    Description: Function used to confirm order and send email
    Parameter:  response : Response object, db : database session, request: User Request.
    Return: Message of order confirmation successfull
    """
    try:
        cart_data = db.query(Cart).filter_by(user_id=request.state.user.id).one_or_none()
        if cart_data is None:
            raise HTTPException(detail='The Cart is Empty', status_code=status.HTTP_400_BAD_REQUEST)
        cart_items_details = db.query(CartItems).filter_by(cart_id=cart_data.id).all()

        message = f"""
            Thank you for confirming the order 
            Total Quantity : {cart_data.total_quantity}
            Total Price is : {cart_data.total_price}    
            Books Details are :
            """
        for data in cart_items_details:
            book_data = db.query(Books).filter_by(id=data.book_id).one_or_none()
            print(book_data.quantity)
            book_data.quantity -= data.quantity
            print(book_data.quantity)
            message += f"Book Name : {book_data.book_name}, Quantity is : {data.quantity}, Total Book Price is :{data.price} \n"

        cart_data.is_ordered = True
        user_data = db.query(Users).filter_by(id=request.state.user.id).one_or_none()
        #send the order confirmation email to the user
        send_confirmation_mail(email=user_data.email, message_body=message)
        db.commit()
        return {'message': 'Order Confirmed Successfully', 'status': 200}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}