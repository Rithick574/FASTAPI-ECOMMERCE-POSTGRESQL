from pydantic import BaseModel, Field

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    username: str = Field(..., min_length=3, max_length=50)
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    username: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True