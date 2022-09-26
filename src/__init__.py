from redis import Redis

from src.auth import router as auth_views
from src.blogs import router as blogs_views
from src.users import router as users_views

__all__ = [blogs_views, users_views, auth_views]

redis_conn = Redis(host='localhost', port=6379, db=0, decode_responses=True)
