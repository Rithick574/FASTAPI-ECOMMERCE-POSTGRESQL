from pydantic import BaseModel
from typing import Optional

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    class Config:
        orm_mode = True 

class CartItemDetailResponse(CartItemResponse):
    product_name: str
    product_description: Optional[str]
    product_price: float

    class Config:
        orm_mode = True 