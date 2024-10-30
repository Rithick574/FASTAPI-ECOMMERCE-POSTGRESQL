from pydantic import BaseModel
from typing import List
import datetime

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    price: float

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    user_id: int

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    total_amount: float
    created_at: datetime.datetime
    items: List[OrderItem]

    class Config:
        orm_mode = True