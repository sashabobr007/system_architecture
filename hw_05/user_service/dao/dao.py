from sqlalchemy import select, Result, and_, func, case, update, delete
from dao.base import BaseDAO
from db import async_session_maker
from models.user import Users
from typing import List, Optional


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def count_models(cls, **filters):
        async with async_session_maker() as session:
            stmt = select(
                func.count(Users.id)
            ).filter_by(**filters)


            result = await session.execute(stmt)
            return result.scalar()

    @classmethod
    async def update(
            cls, username : str, **data
    ):

        async with async_session_maker() as session:

            stmt = (
                update(Users)
                .where(Users.username == username)
                .values(**data)
            )

            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def find_by_id(cls, id):
        async with async_session_maker() as session:
            query = select(Users).filter_by(id=id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def search_users(
            cls
    ):
        async with async_session_maker() as session:
            query = select(Users)
            result: Result = await session.execute(query)
            return result.mappings().all()


    @classmethod
    async def delete(cls, username):

        async with async_session_maker() as session:

            stmt = (
                delete(
                    Users
                )
                .where(
                    Users.username == username
                )
            )

            await session.execute(stmt)
            await session.commit()