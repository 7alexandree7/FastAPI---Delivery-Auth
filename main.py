from fastapi import FastAPI
from dotenv import load_dotenv
from passlib.context import CryptContext
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from auth_routes import auth_route
from order_routes import order_route

app.include_router(auth_route)
app.include_router(order_route)
