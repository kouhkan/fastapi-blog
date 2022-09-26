from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from src.auth.schemas import Auth
from src.database import get_db
from src.users.models import User
from src.users.utils import Hash

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/")
def auth(request: Auth, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{request.username} not found")

    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Password")

    access_token = Authorize.create_access_token(subject=user.username)
    refresh_token = Authorize.create_refresh_token(subject=user.username)
    return {"access": access_token, "refresh": refresh_token}


@router.put("/")
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=current_user)

    return {"access": access_token}


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def access_revoke(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    jti = Authorize.get_raw_jwt()['jti']
    from src import redis_conn
    from src.auth.config import settings
    redis_conn.setex(jti, settings.access_expires, 'true')

    return {}
