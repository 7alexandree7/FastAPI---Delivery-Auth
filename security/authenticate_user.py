from fastapi import HTTPException
from models.models import User
from main import bcrypt_context


def authenticate_user(email, password, session):
    user = session.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    elif not bcrypt_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="invalid password")

    return user