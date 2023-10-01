from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

class UserBase(BaseModel):
    user_name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserInDB(UserBase):
    id: int
    date_registered: Optional[datetime]

    class Config:
        crm_mode = True


class UserResponse(UserInDB):
    pass