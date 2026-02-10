from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base


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

    #STATUS_CHOICE = (("pendente", "pendente"), ("cancelado", "cancelado"), ("finalizado", "finalizado"))

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    status = Column("status", String) #pendente, cancelado, finalizado
    user = Column("user", ForeignKey("users.id")) 
    price = Column("price", Float)

    def __init__ (self, user, status="pendente", price=0):
        self.user = user
        self.status = status
        self.price = price


class OrderedItem(Base):
    __tablename__ = "ordered_items"

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    quantity = Column("quantity", Integer)
    flavor = Column("flavor", String)
    size = Column("size", String)
    unit_price = Column("unit_price", Float)
    order = Column("order", ForeignKey("orders.id"))

    def __init__ (self, quantity, falvor, size, unit_price, order):
        self.quantity = quantity
        self.flavor = falvor
        self.size = size
        self.unit_price = unit_price
        self.order = order