from datetime import datetime

from sqlalchemy import Column, Integer, Text, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer(), primary_key=True, index=True)
    title = Column(String(length=150), nullable=False, unique=False)
    slug = Column(String(length=150), nullable=False, unique=True)
    body = Column(Text(), nullable=False, unique=False)
    draft = Column(Boolean)
    created_at = Column(DateTime(), nullable=False, unique=False, default=datetime.utcnow)
    updated_at = Column(DateTime(), nullable=False, unique=False, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="blogs")
