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
    def __repr__(self):
        return self.user_name
    

class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(BigInteger, primary_key=True, index=True)
    request_method = Column(String)
    request_path = Column(String)
    count = Column(BigInteger, default=1)

    