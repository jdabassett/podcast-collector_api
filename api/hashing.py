from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash:
    @staticmethod
    def bcrypt(password: str) -> str:
        """Accept string password and return hashed password."""
        return pwd_context.hash(password)

    @staticmethod
    def verify(request_password: str, hashed_password: str) -> bool:
        """Accepts unhashed password and hashed password. Returns boolean if password is identical."""
        return pwd_context.verify(request_password, hashed_password)
