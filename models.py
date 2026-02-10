from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base

db = create_engine("sqlite:///db/database.db")

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"

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