from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.order import OrderCreate, OrderResponse
from app.models.order import Order, OrderItem
from app.utils.auth import get_current_user
from app.models.user import User 
from app.database from get_db

router = APIRouter()

@router.post("/orders", response_model=OrderResponse)
async def create_order(
    order: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_order = Order(user_id=current_user.id, total_amount=order.total_amount)
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)  

    for item in order.items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        db.add(order_item)

    await db.commit()  
    return new_order 

@router.get("/orders", response_model=list[OrderResponse])
async def list_orders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Order).where(Order.user_id == current_user.id)
    result = await db.execute(query)
    orders = result.scalars().all()
    return orders 

@router.get("/orders/{order_id}", response_model=OrderResponse)
async def read_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Order).where(Order.id == order_id, Order.user_id == current_user.id)
    result = await db.execute(query)
    order = result.scalar_one_or_none()
    
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order

@router.put("/orders/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Order).where(Order.id == order_id, Order.user_id == current_user.id)
    result = await db.execute(query)
    db_order = result.scalar_one_or_none()
    
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db_order.total_amount = order.total_amount 
    await db.commit()
    await db.refresh(db_order)
    return db_order

@router.delete("/orders/{order_id}", response_model=OrderResponse)
async def delete_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Order).where(Order.id == order_id, Order.user_id == current_user.id)
    result = await db.execute(query)
    db_order = result.scalar_one_or_none()
    
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    await db.delete(db_order) 
    await db.commit()
    return db_order 