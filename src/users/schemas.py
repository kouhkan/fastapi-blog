from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: Optional[str] = None
    password: str
    is_active: bool = False
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
