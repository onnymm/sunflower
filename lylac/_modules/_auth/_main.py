from typing import Literal
from passlib.context import CryptContext
from ..._constants import MODEL_NAME, MESSAGES
from ..._core import ENV_VARIABLES
from ..._core.modules import Auth_Core
from ..._core.main import _Lylac_Core
from ...errors import InvalidPasswordError
from ._submodules import (
    Token,
    UserSession,
)

class Auth(Auth_Core):

    def __init__(
        self,
        instance: _Lylac_Core
    ) -> None:

        # Asignación de instancia principal
        self._main = instance
        # Asignación de instancia de compilar
        self._compiler = instance._compiler
        # Inicialización de submódulos
        self._m_session = UserSession(self)
        self._m_token = Token(self)

        # Contexto para hasheo
        self._pwd_context = CryptContext(schemes= ['bcrypt'], deprecated= 'auto')

    def identify_user(
        self,
        token: str,
    ) -> int:

        # Obtención de la UUID de la sesión
        session_uuid = self._m_token.get_session_uuid_from_token(token)
        # Obtención de la ID del usuario desde la UUID de la sesión
        user_id = self._m_session.get_session_uuid_user_id(session_uuid)

        return user_id

    def hash_password(
        self,
        password: str,
    ) -> str:

        # Se genera el hasheo de la contraseña
        hashed_password = self._pwd_context.hash(password)

        return hashed_password

    def login(
        self,
        login: str,
        password: str,
    ) -> str | Literal[False]:

        # Obtención de la ID del usuario si las credenciales son correctas
        user_id = self._authenticate_user_by_login(login, password)
        # Si las credenciales son correctas...
        if user_id:

            # Generación de la UUID de sesión y su fecha de expiración
            ( session_uuid, expiration_date ) = self._m_session.generate_user_session(user_id)
            # Se crea un token de sesión
            token = self._m_token.create_session_token(session_uuid, expiration_date)

            return token

        # Si las credenciales no son correctas...
        else:
            return False

    def reset_password(
        self,
        user_id: int,
    ) -> None:

        # Obtención de la contraseña genérica inicial
        default_password = ENV_VARIABLES.DEFAULT.PASSWORD
        # Se hashea la contraseña
        hashed_password = self.hash_password(default_password)
        # Se ejecuta la transacción en la base de datos
        self._compiler.change_password(user_id, hashed_password)
        # Se cierran las sesiones
        self._close_sessions(user_id)

    def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str,
        close_sessions: bool = True,
    ) -> None:

        # Verificación de la contraseña actual
        self._authenticate_user_by_id(user_id, old_password)
        # Se hashea la nueva contraseña
        hashed_new_password = self.hash_password(new_password)
        # Se realiza el cambio de contraseña
        self._compiler.change_password(user_id, hashed_new_password)

        # Si se especificó que se deben cerrar las sesiones anteriores...
        if close_sessions:
            # Se cierran las sesiones
            self._close_sessions(user_id)

    def _close_sessions(
        self,
        user_id: int,
    ) -> None:

        # Obtención de las IDs de las sesiones anteriores
        session_ids = self._main.search(
            self._main._ROOT_USER,
            MODEL_NAME.BASE_USERS_SESSION,
            [('user_id', '=', user_id)],
        )
        # Se eliminan éstas
        self._main.delete(
            self._main._ROOT_USER,
            MODEL_NAME.BASE_USERS_SESSION,
            session_ids,
        )

    def _authenticate_user_by_id(
        self,
        user_id: int,
        password: str,
    ) -> None:

        # Obtención de la contraseña hasheada desde la base de datos
        hashed_password_from_db= self._main.get_value(
            self._main._ROOT_USER,
            MODEL_NAME.BASE_USERS,
            user_id,
            'password',
        )
        # Verificación de la contraseña
        is_correct_password = self._verify_password(password, hashed_password_from_db)
        # Si la contraseña es incorrecta
        if not is_correct_password:
            # Se arroja el error de contraseña inválida
            raise InvalidPasswordError(MESSAGES.ACCOUNT.WRONG_PASSWORD)

    def _authenticate_user_by_login(
        self,
        login: str,
        password: str,
    ) -> int | Literal[False]:

        # Obtención de los datos del usuario
        found_data = self._compiler.get_user_data_by_username(login)

        # Si no se encontraron datos...
        if found_data is None:
            # Se retorna falso
            return False

        # Destructuración de los datos
        ( user_id, hashed_password_from_db ) = found_data

        # Verificación de la contraseña
        is_correct_password = self._verify_password(password, hashed_password_from_db)
        # Si la contraseña es incorrecta
        if not is_correct_password:
            # Se arroja el error de contraseña inválida
            raise InvalidPasswordError(MESSAGES.ACCOUNT.WRONG_PASSWORD)
        # Si la contraseña es incorrecta...
        else:
            # Se retorna falso
            return user_id

    def _verify_password(
        self,
        typed_password: str,
        hashed_password_from_db,
    ) -> bool:

        # Verificación de la contraseña
        verified = self._pwd_context.verify(typed_password, hashed_password_from_db)

        return verified
