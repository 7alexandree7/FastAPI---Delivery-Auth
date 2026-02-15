from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    is_active: Optional[bool] = None
    admin: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }

class LoginSchema(BaseModel):
    email: str
    password: str

    model_config = {
        "from_attributes": True
    }

class OrderSchema(BaseModel):
    user: int
    
    model_config = {
        "from_attributes": True
    }


class OrderedItemSchema(BaseModel):
    quantity: int
    flavor: str
    size: str
    unit_price: float

    model_config = {
        "from_attributes": True
    }



class ResponseOrderSchema(BaseModel):
    id: int
    status: str
    price: float

    model_config = {
        "from_attributes": True
    }