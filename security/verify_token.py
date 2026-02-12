from fastapi import Depends
from models.models import User
from sqlalchemy.orm import Session
from db.session import get_session


def verify_token(token, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.id == 1).first()
    return user
