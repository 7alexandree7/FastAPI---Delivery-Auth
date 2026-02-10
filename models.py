from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

db = create_engine("sqlite:///db/database.db")

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    name = Column("name", String)
    email = Column("email", String, nullable=False)
    password = Column("password", String)
    is_active = Column("is_active", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__ (self, name, email, password, is_active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.is_active = is_active
        self.admin = admin


class Order(Base):
    __tablename__ = "orders"

    STATUS_CHOICE = (("pendente", "pendente"), ("cancelado", "cancelado"), ("finalizado", "finalizado"))

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    status = Column("status", ChoiceType(choices=STATUS_CHOICE)) #pendente, cancelado, finalizado
    user = Column("user", ForeignKey("users.id")) 
    price = Column("price", Float)

    def __init__ (self, user, status="pendente", price=0):
        self.user = user
        self.status = status
        self.price = price