from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BIGINT, TEXT, BOOLEAN, ForeignKey
from sqlalchemy import Column, Integer, String

from db import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, index=True)
    role = Column(String)
    hashed_password = Column(String)
