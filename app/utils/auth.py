from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.utils.security import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    user_data = verify_token(token)  
    
    if user_data is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = await db.get(User, user_data["sub"]) 
    if user is None:
        raise HTTPException(status_code=404, detail="User  not found")
    
    return user