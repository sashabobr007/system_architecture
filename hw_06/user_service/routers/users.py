from fastapi import APIRouter, Depends, HTTPException, Query, Request
from auth.dependencies import get_current_user, check_owner_permissions,create_access_token
from models.user import *
from passlib.context import CryptContext
from typing import List, Optional
from exceptions import (UserNotEnoughPermissions, UserNotFoundException, UserAlreadyExistsException,
                                           UserNameAlreadyExistsException, UserNotDeleteSelf)

from schemas.schemas import UserCreate, UserInDB,  UserBase, UserUpdate, UserRole
from dao.dao import UsersDAO
import redis
import os
import json
from confluent_kafka import Producer
from pydantic import UUID4
import uuid

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

conf = {'bootstrap.servers': 'kafka1:9092,kafka2:9092'}
producer = Producer(conf)
# Функция для обработки результатов доставки сообщения
def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')


def get_user_cache_key(user_id: int) -> str:
    return f"user:id:{user_id}"

def get_username_cache_key(username: str) -> str:
    return f"user:username:{username}"

def get_search_cache_key(first_name: str, last_name: str) -> str:
    return f"users:search:{first_name}:{last_name}"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/create_user", response_model=UserInDB)
async def create_user(
        user: UserCreate):
    # Проверка существующего пользователя
    existing_user = await UsersDAO.find_one_or_none(username=user.username)
    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = pwd_context.hash(user.password)

    # Формирование данных пользователя
    user_data = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'role': user.role,
        'hashed_password': hashed_password
    }

    # Отправка сообщения в Kafka
    producer.produce(
        topic='user_created',
        value=json.dumps(user_data).encode('utf-8'),
        callback=delivery_report
    )
    producer.poll(0)  # Неблокирующая обработка

    # Кеширование в Redis
    cache_key = get_username_cache_key(user_data['username'])
    redis_client.set(cache_key, json.dumps(user_data), ex=10)

    return UserInDB(**user_data)
#
# # Создание пользователя
# @router.post("/create_user", response_model=UserInDB)
# async def create_user(user: UserCreate):
#     existing_user = await UsersDAO.find_one_or_none(username=user.username)
#     if existing_user:
#         raise UserAlreadyExistsException
#
#     hashed_password = pwd_context.hash(user.password)
#     user_data = {
#         'username': user.username,
#         'first_name': user.first_name,
#         'last_name': user.last_name,
#         'email': user.email,
#         'role': user.role,
#         'hashed_password': hashed_password
#     }
#
#     new_user = await UsersDAO.add(**user_data)
#     cache_key = get_user_cache_key(new_user.id)
#     existing_user = await UsersDAO.find_one_or_none(id=new_user.id)
#     redis_client.set(
#         cache_key,
#         json.dumps(str(existing_user)),
#         ex=180  # Время жизни кеша 3 минуты
#     )
#     return new_user


# Поиск пользователя по id с кешированием
@router.get("/{user_id}", response_model=UserInDB)
async def read_user_by_id(
        user_id: int
):
    cache_key = get_user_cache_key(user_id)
    # Проверяем кеш
    if redis_client.exists(cache_key):
        cached_user = json.loads(redis_client.get(cache_key))
        cached_user = cached_user.replace("'", '"')
        cached_user = json.loads(cached_user)
        return cached_user

    # Ищем в базе
    existing_user = await UsersDAO.find_one_or_none(id=user_id)
    if not existing_user:
        raise UserNotFoundException

    redis_client.set(
        cache_key,
        json.dumps(str(existing_user)),
        ex=180  # Время жизни кеша 3 минуты
    )
    return existing_user


# Получение информации о текущем пользователе (с кешированием)
@router.get("/get_self/", response_model=UserInDB)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    print(current_user)
    cache_key = get_user_cache_key(current_user.id)
    print(cache_key)
    if redis_client.exists(cache_key):
        cached_data = json.loads(redis_client.get(cache_key))
        cached_user = cached_data.replace("'", '"')
        cached_user = json.loads(cached_user)
        return cached_user
    redis_client.set(cache_key, json.dumps(str(current_user)), ex=300)
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
@router.get("/{username}/", response_model=UserInDB)
async def read_user_by_username(
        username: str,
        current_user: UserInDB = Depends(get_current_user)
):
    cache_key = get_username_cache_key(username)

    if redis_client.exists(cache_key):
        cached_data = json.loads(redis_client.get(cache_key))
        cached_user = cached_data.replace("'", '"')
        cached_user = json.loads(cached_user)
        # Проверка прав доступа
        if current_user.role != UserRole.OWNER and current_user.username != cached_user.username:
            raise UserNotEnoughPermissions
        return cached_user

    existing_user = await UsersDAO.find_one_or_none(username=username)
    if not existing_user:
        raise UserNotFoundException

    # Проверка прав доступа
    if current_user.role != UserRole.OWNER and current_user.username != username:
        raise UserNotEnoughPermissions

    redis_client.set(cache_key, json.dumps(str(existing_user)), ex=180)
    return existing_user

# # Поиск пользователей по имени/фамилии
@router.get("/user/search/", response_model=List[UserInDB])
async def search_users(
        first_name: Optional[str] = Query(None, min_length=1),
        last_name: Optional[str] = Query(None, min_length=1),
    current_user: UserInDB = Depends(get_current_user)
):
    users = await UsersDAO.find_all()
    results = []
    for user in users:
        if first_name and first_name.lower() not in user.first_name.lower():
            continue
        if last_name and last_name.lower() not in user.last_name.lower():
            continue
        results.append(user)
    return results


# Обновление пользователя
@router.put("/{username}", response_model=UserUpdate)
async def update_user(
        username: str,
        user_update: UserUpdate,
        current_user: UserInDB = Depends(get_current_user)
):
    existing_user = await UsersDAO.find_one_or_none(username=username)
    if not existing_user:
        raise UserNotFoundException

    if current_user.role != UserRole.OWNER and current_user.username != username:
        raise UserNotEnoughPermissions

    user_data = {}
    if user_update.first_name:
        user_data['first_name'] = user_update.first_name
    if user_update.last_name:
        user_data['last_name'] = user_update.last_name
    if user_update.email:
        user_data['email'] = user_update.email
    updated_user = await UsersDAO.update(username=username, **user_data)

    # Инвалидация кешей
    redis_client.delete(
        get_user_cache_key(existing_user.id),
        get_username_cache_key(username)
    )
    return user_update


# Удаление пользователя
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

    await UsersDAO.delete(username)

    # Инвалидация всех связанных кешей
    redis_client.delete(
        get_user_cache_key(existing_user.id),
        get_username_cache_key(username)
    )
    return {"message": f"User {username} deleted"}