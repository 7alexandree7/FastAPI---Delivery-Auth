from fastapi import HTTPException, Depends
from models.models import User
from main import bcrypt_context, ACCESS_TOKEN_EXPIRES_MINUTES, SECRET_KEY, ALGORITHM
from jose import jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from db.session import get_session


def create_token(id_user, duration_token=timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)):
    expiration_date = datetime.now(timezone.utc) + duration_token
    dic_info = { "sub": id_user, "exp": expiration_date }
    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.id == 1).first()
    return user



def authenticate_user(email, password, session):
    user = session.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    elif not bcrypt_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="invalid password")

    return user