from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from .models import User
from .schemas import User as UserSchema
from .schemas import UserOut
from .utils import Hash
from ..database import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserOut)
def create_user(request: UserSchema, db: Session = Depends(get_db)):
    user = User()

    for key, value in request.__dict__.items():
        setattr(user, key, value)
    user.password = Hash.bcrypt(request.password)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get("/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user
