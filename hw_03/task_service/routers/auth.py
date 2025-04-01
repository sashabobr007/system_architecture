from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth.dependencies import create_access_token

from passlib.context import CryptContext
from exceptions import InvalidCredentialsException
from datetime import datetime, timedelta
from core.config import settings
from models.user import UserInDB, UserRole

# для удобного теста в swagger
fake_users_db = {
    "admin": UserInDB(
        id=1,
        username="admin",
        first_name="Admin",
        last_name="User",
        email="admin@example.com",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
        role=UserRole.OWNER,
        disabled=False
    ),
    "user1": UserInDB(
        id=2,
        username="user1",
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
        role=UserRole.USER,
        disabled=False
    )
}

router = APIRouter(prefix="/auth", tags=["Auth/Token"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise InvalidCredentialsException
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}