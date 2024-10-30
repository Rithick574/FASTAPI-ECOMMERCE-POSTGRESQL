from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    
class UserCreate(UserBase):
    username: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True