from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.orm import Session

from src.blogs.models import Blog
from src.blogs.schemas import Blog as BlogSchema
from src.blogs.schemas import BlogOut
from src.database import get_db

router = APIRouter(prefix="/blogs", tags=["blogs"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: BlogSchema, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    blog = Blog()

    for key, value in request.__dict__.items():
        setattr(blog, key, value)
    db.add(blog)
    db.commit()
    db.refresh(blog)

    return blog


@router.get("/", response_model=List[BlogOut], tags=["blogs"])
def all_blogs(db: Session = Depends(get_db)):
    return db.query(Blog).all()


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=BlogOut)
def single(id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found")

    return blog


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).delete(synchronize_session=False)

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found")

    db.commit()

    return {}


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: BlogSchema, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found")

    for key, value in request.__dict__.items():
        setattr(blog, key, value)

    db.commit()

    return blog
