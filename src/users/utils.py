from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    @staticmethod
    def bcrypt(password: str) -> str:
        return pwd_cxt.hash(password)

    @staticmethod
    def verify(request_password: str, user_password: str) -> bool:
        return pwd_cxt.verify(request_password, user_password)
