from fastapi import APIRouter, Depends, HTTPException, Query
from hw_02.user_service.auth.dependencies import get_current_user, check_owner_permissions,create_access_token
from hw_02.user_service.models.user import *
from hw_02.user_service.db.fake_db import fake_users_db
from passlib.context import CryptContext
from typing import List, Optional
from hw_02.user_service.exceptions import (UserNotEnoughPermissions, UserNotFoundException, UserAlreadyExistsException,
                                           UserNameAlreadyExistsException)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/user", tags=["Users"])

@router.get("/me", response_model=UserInDB)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user

@router.post("/create_user", response_model=UserInDB)
async def create_user(user: UserCreate):
    if user.username in fake_users_db:
        raise UserNameAlreadyExistsException
    hashed_password = pwd_context.hash(user.password)
    db_user = UserInDB(**user.dict(), id=len(fake_users_db)+1, hashed_password=hashed_password)
    fake_users_db[user.username] = db_user
    return db_user

# Получение всех пользователей (только для владельцев)
@router.get("/", response_model=List[UserInDB])
async def read_all_users(
        current_user: UserInDB = Depends(get_current_user)
):
    await check_owner_permissions(current_user)
    return list(fake_users_db.values())


# Поиск пользователя по username
@router.get("/{username}", response_model=UserInDB)
async def read_user_by_username(
        username: str,
        current_user: UserInDB = Depends(get_current_user)
):
    if username not in fake_users_db:
        raise UserNotFoundException

    # Владельцы могут смотреть любого, обычные пользователи - только себя
    if current_user.role != UserRole.OWNER and current_user.username != username:
        raise UserNotEnoughPermissions

    return fake_users_db[username]


# Поиск пользователей по имени/фамилии
@router.get("/search/", response_model=List[UserInDB])
async def search_users(
        first_name: Optional[str] = Query(None, min_length=1),
        last_name: Optional[str] = Query(None, min_length=1),
        current_user: UserInDB = Depends(get_current_user)
):
    results = []
    for user in fake_users_db.values():
        if first_name and first_name.lower() not in user.first_name.lower():
            continue
        if last_name and last_name.lower() not in user.last_name.lower():
            continue
        results.append(user)
    return results


# Обновление пользователя
@router.put("/{username}", response_model=UserInDB)
async def update_user(
        username: str,
        user_update: UserUpdate,
        current_user: UserInDB = Depends(get_current_user)
):
    if username not in fake_users_db:
        raise UserNotFoundException

    # Владельцы могут обновлять любого, обычные пользователи - только себя
    if current_user.role != UserRole.OWNER and current_user.username != username:
        raise UserNotEnoughPermissions

    db_user = fake_users_db[username]
    update_data = user_update.dict(exclude_unset=True)
    updated_user = db_user.copy(update=update_data)
    fake_users_db[username] = updated_user
    return updated_user


# Удаление пользователя (только для владельцев)
@router.delete("/{username}")
async def delete_user(
        username: str,
        current_user: UserInDB = Depends(get_current_user)
):
    await check_owner_permissions(current_user)

    if username not in fake_users_db:
        raise UserNotFoundException

    if current_user.username == username:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")

    deleted_user = fake_users_db.pop(username)
    return {"message": f"User {username} deleted", "user": deleted_user}