from fastapi import APIRouter, Depends, HTTPException
from db.session import get_session
from schema.schemas import OrderSchema, OrderedItemSchema
from sqlalchemy.orm import Session
from models.models import Order, User, OrderedItem
from security.verify_token import verify_token


order_route = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(verify_token)])

@order_route.get("/")
async def get_orders():
    return {"messagem": "voce acessou a rota de orders"}


@order_route.post("/order")
async def create_order(orderSchema: OrderSchema, session: Session = Depends(get_session)):
    try:
        new_order = Order(user=orderSchema.user)
        session.add(new_order)
        session.commit()
        session.refresh(new_order)

        return {"message": f"order created {new_order.id}"}
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="error creating order")


@order_route.post("/order/cancel/{order_id}")
async def cancel_order(order_id: int, user: User = Depends(verify_token), session: Session = Depends(get_session)):

    order = session.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    
    if not (user.admin or order.user == user.id):
        raise HTTPException(status_code=403, detail="you dont have permission to cancel this order")
    
    order.status = "cancelado"
    session.commit()

  
    return {
        "message": f"order {order.id} canceled",
        "order": order,
        "user": f"Pedido cancelado por {user.name}"
    }


@order_route.get("/list")
async def list_orders(user: User = Depends(verify_token), session: Session = Depends(get_session)):

    if not user.admin:
        raise HTTPException(status_code=403, detail="you dont have permission to list orders")
    
    else:
        orders = session.query(Order).all()
        return {"orders": orders}


@order_route.post("order/add-item/{order_id}")
async def add_item_to_order(order_id: int, orderedItemSchema: OrderedItemSchema, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    
    if not (user.admin or user.id == order.user):
        raise HTTPException(status_code=403, detail="you dont have permission to add item to this order")
    
    order_item = OrderedItem(
        orderedItemSchema.quantity,
        orderedItemSchema.flavor,
        orderedItemSchema.size,
        orderedItemSchema.unit_price,
        order.id
    )

    session.add(order_item)
    order.calculate_price()
    session.commit()

    return {
        "message": "Item added sucessfully",
        "item_id": order_item.id,
        "order_price": order.price
    }