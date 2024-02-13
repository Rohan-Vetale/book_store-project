"""
@Author: Rohan Vetale

@Date: 2024-02-09 12:40

@Last Modified by: Rohan Vetale

@Last Modified time: 2024-02-09 18:50

@Title : Book Store's Model module
"""

from sqlalchemy.orm import declarative_base, Session, relationship
from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, String, Table, create_engine, Text
from core.settings import DATABASE_DIALECT, DATABASE_DRIVER, DATABASE_NAME, DATABASE_PASSWORD, DATABASE_USERNAME, DEFAULT_PORT, HOST

database_url = f"{DATABASE_DIALECT}+{DATABASE_DRIVER}://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{HOST}:{DEFAULT_PORT}/{DATABASE_NAME}"
engine = create_engine(database_url)
session = Session(engine)
Base = declarative_base()

def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()

class Users(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String(50), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50))
    email = Column(String(50), unique=True)
    phone = Column(BigInteger)
    state = Column(String(100))
    password = Column(String(100))
    is_verified = Column(Boolean, default=False)
    is_super_user = Column(Boolean, default=False)
    books = relationship('Books', back_populates='users')
    cart = relationship('Cart', back_populates='users')
    def __repr__(self):
        return self.user_name
    
class Books(Base):
    __tablename__ = "books"
    id = Column(BigInteger, primary_key=True, index=True)
    book_name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    price = Column(BigInteger, nullable=False)
    quantity = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    users = relationship('Users', back_populates='books') 
    cart_items = relationship('CartItems', back_populates='book')



class RequestLog(Base):
    __tablename__ = "request_logs"
    id = Column(BigInteger, primary_key=True, index=True)
    request_method = Column(String)
    request_path = Column(String)
    count = Column(BigInteger, default=1)

class Cart(Base):
    __tablename__ = 'cart'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    total_price = Column(BigInteger, default=0)
    total_quantity = Column(BigInteger, default=0)
    is_ordered = Column(Boolean, default=False)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    users = relationship('Users', back_populates='cart')
    cart_items = relationship('CartItems', back_populates='cart')
    
    
class CartItems(Base):
    __tablename__ = 'cart_items'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    price = Column(BigInteger, default=0)
    quantity = Column(BigInteger, default=0)
    book_id = Column(BigInteger, ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    cart_id = Column(BigInteger, ForeignKey('cart.id', ondelete='CASCADE'), nullable=False)
    book = relationship('Books', back_populates='cart_items')
    cart = relationship('Cart', back_populates='cart_items')