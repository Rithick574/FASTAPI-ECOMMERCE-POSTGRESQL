from pydantic import BaseModel
from typing import List
import datetime

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
     price: float

class OrderCreate(BaseModel):
    total_amount: float
    items: List[OrderItemCreate]

class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: float

    class Config:
        orm_mode = True 

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    created_at: datetime.datetime
    items: List[OrderItemResponse]

    class Config:
        orm_mode = True