from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True, index=True)
    username = Column(String(64), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=True, unique=True)
    password = Column(String(300), nullable=False, unique=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(), nullable=False, unique=False, default=datetime.utcnow)
    updated_at = Column(DateTime(), nullable=False, unique=False, default=datetime.utcnow)
    blogs = relationship("Blog", back_populates="author")
