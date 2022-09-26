from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.users.schemas import UserOut


class Blog(BaseModel):
    title: str
    slug: Optional[str] = None
    body: str
    user_id: Optional[int]
    draft: bool = True
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

    class Config:
        orm_mode = True


class BlogOut(BaseModel):
    id: int
    title: str
    author: UserOut

    class Config:
        orm_mode = True
