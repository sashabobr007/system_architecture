import json

from passlib.context import CryptContext
from sqlalchemy import select, insert, Result, func

from datetime import datetime

from typing import Any

from db import async_session_maker


class BaseDAO:

    model = None

    @classmethod
    async def find_by_id(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result: Result = await session.execute(query)
            return result.mappings().first()

    @classmethod
    async def find_all(cls, **data):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**data)
            result: Result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result: Result = await session.execute(query)
            return result.mappings().first()
            # return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar()
