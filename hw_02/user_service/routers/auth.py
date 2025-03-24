from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from hw_02.user_service.auth.dependencies import create_access_token
from hw_02.user_service.db.fake_db import fake_users_db
from passlib.context import CryptContext
from hw_02.user_service.exceptions import InvalidCredentialsException
from datetime import datetime, timedelta
from hw_02.user_service.core.config import settings


router = APIRouter(prefix="/auth", tags=["Auth/Token"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise InvalidCredentialsException
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}