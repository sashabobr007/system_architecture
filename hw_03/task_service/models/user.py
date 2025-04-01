from enum import Enum
from pydantic import BaseModel

class UserRole(str, Enum):
    USER = "user"
    OWNER = "owner"

class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    role: UserRole = UserRole.USER
    disabled: bool = False

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    disabled: bool | None = None

class UserInDB(UserBase):
    id: int
    hashed_password: str