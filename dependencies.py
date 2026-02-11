from sqlalchemy.orm import sessionmaker
from models import db

def get_session ():
    try:
        session =  sessionmaker(bind=db)
        session = session()
        yield session

    finally:
        session.close()