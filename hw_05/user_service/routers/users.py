from fastapi import APIRouter, Depends, HTTPException, Query
from auth.dependencies import get_current_user, check_owner_permissions,create_access_token
from models.user import *
from passlib.context import CryptContext
from typing import List, Optional
from exceptions import (UserNotEnoughPermissions, UserNotFoundException, UserAlreadyExistsException,
                                           UserNameAlreadyExistsException, UserNotDeleteSelf)

from schemas.schemas import UserCreate, UserInDB,  UserBase, UserUpdate, UserRole
from dao.dao import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/user", tags=["Users"])

# Создание пользователя
@router.post("/create_user", response_model=UserInDB)
async def create_user(user: UserCreate):
    existing_user = await UsersDAO.find_one_or_none(username=user.username)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = pwd_context.hash(user.password)
    user_data = {   'username' : user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'role': user.role,
                    'hashed_password' : hashed_password}
    user = await UsersDAO.add(**user_data)
    return user

# Поиск пользователя по id
@router.get("/{user_id}", response_model=UserInDB)
async def read_user_by_id(
        user_id: int):
    existing_user = await UsersDAO.find_one_or_none(id=user_id)
    if not existing_user:
        raise UserNotFoundException
    return existing_user

# Получение информации о текущем пользователе
@router.get("/me", response_model=UserInDB)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user


# Получение всех пользователей (только для владельцев)
@router.get("/", response_model=List[UserInDB])
async def read_all_users(
        current_user: UserInDB = Depends(get_current_user)
):
    await check_owner_permissions(current_user)
    users = await UsersDAO.find_all()
    return users


# Поиск пользователя по username
@router.get("/{username}", response_model=UserInDB)
async def read_user_by_username(
        username: str,
        current_user: UserInDB = Depends(get_current_user)
):
    existing_user = await UsersDAO.find_one_or_none(username=username)
    if not existing_user:
        raise UserNotFoundException

    # Владельцы могут смотреть любого, обычные пользователи - только себя
    if current_user.role != UserRole.OWNER and current_user.username != username:
        raise UserNotEnoughPermissions

    return existing_user


# # Поиск пользователей по имени/фамилии
@router.get("/search/", response_model=List[UserInDB])
async def search_users(
        first_name: Optional[str] = Query(None, min_length=1),
        last_name: Optional[str] = Query(None, min_length=1),
        current_user: UserInDB = Depends(get_current_user)
):
    users = await UsersDAO.find_all()
    results = []
    for user in users:
        print(user)
        if first_name and first_name.lower() not in user.first_name.lower():
            continue
        if last_name and last_name.lower() not in user.last_name.lower():
            continue
        results.append(user)
    return results

#
# # Обновление пользователя
@router.put("/{username}", response_model=UserUpdate)
async def update_user(
        username: str,
        user_update: UserUpdate,
       current_user: UserInDB = Depends(get_current_user)
):
    existing_user = await UsersDAO.find_one_or_none(username=username)
    if not existing_user:
        raise UserNotFoundException

    #Владельцы могут обновлять любого, обычные пользователи - только себя
    if current_user.role != UserRole.OWNER and current_user.username != username:
        raise UserNotEnoughPermissions
    user_data = {}
    if user_update.first_name:
        user_data['first_name'] = user_update.first_name
    if user_update.last_name:
        user_data['last_name'] = user_update.last_name
    if user_update.email:
        user_data['email'] = user_update.email
    print(user_data)
    updated_user = await UsersDAO.update(username=username, **user_data)
    return user_update


# Удаление пользователя (только для владельцев)
@router.delete("/{username}")
async def delete_user(
        username: str,
        current_user: UserInDB = Depends(get_current_user)
):
    await check_owner_permissions(current_user)

    existing_user = await UsersDAO.find_one_or_none(username=username)
    if not existing_user:
        raise UserNotFoundException

    if current_user.username == username:
        raise UserNotDeleteSelf

    deleted_user = await UsersDAO.delete(username)
    return {"message": f"User {username} deleted"}