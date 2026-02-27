from passlib.context import CryptContext
from .._settings._users import SETTINGS

_pwd_context = CryptContext(schemes= ['bcrypt'], deprecated= 'auto')

def hash_password(password: str) -> str:
    """
    Obtención de hash de contraseña.
    """
    return _pwd_context.hash(password)

def default_password() -> str:
    return hash_password(SETTINGS.DEFAULT_PASSWORD)
