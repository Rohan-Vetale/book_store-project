"""
@Author: Rohan Vetale

@Date: 2024-01-28 19:44

@Last Modified by: Rohan Vetale

@Last Modified time: 2024-01-28 19:22

@Title : Fundoo Notes using FastAPI
"""
from fastapi import FastAPI, Security, Depends, Request
from fastapi.security import APIKeyHeader
from core.utils import jwt_authentication, request_loger
from routes.user import router_user
from routes.book import router_books
from routes.cart import router_cart


app = FastAPI()
@app.middleware("http")
def addmiddleware(request: Request, call_next):
    response = call_next(request)
    request_loger(request)
    return response

app.include_router(router_user, prefix='/user')
app.include_router(router_books, prefix='/book',dependencies=[Security(APIKeyHeader(name='authorization')),Depends(jwt_authentication)])
app.include_router(router_cart, prefix='/cart',dependencies=[Security(APIKeyHeader(name='authorization')),Depends(jwt_authentication)])

