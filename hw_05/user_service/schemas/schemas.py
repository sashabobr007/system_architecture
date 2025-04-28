from enum import Enum
from pydantic import BaseModel


class UserRole(str, Enum):
    USER = "user"
    OWNER = "owner"
#
class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    role: UserRole = UserRole.USER
#
class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    first_name: str | None
    last_name: str | None
    email: str | None

class UserInDB(UserBase):
   # id: int
    hashed_password: str