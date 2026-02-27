from uuid import uuid4
from datetime import (
    datetime,
    timedelta,
)
from ...._constants import (
    FIELD_NAME,
    MODEL_NAME,
    ROOT_ID,
)
from ...._core.submods.auth import _Session_Interface
from ...._core.modules import Auth_Core
from ...._settings import SESSION

class UserSession(_Session_Interface):
    _auth: Auth_Core

    def __init__(
        self,
        instance: Auth_Core,
    ) -> None:

        # Asignación de instancia propietaria
        self._auth = instance
        # Asignación de instancia principal
        self._main = instance._main
        # Referencia del módulo de compilador
        self._compiler = instance._main._compiler
        # Referencia del módulo de manipulación de datos
        self._dml = instance._main._dml

    def generate_user_session(
        self,
        user_id: int,
    ) -> tuple[str, datetime]:

        # Generación de la fecha de expiración del token
        expiration_date = self._generate_token_expiration_date()
        # Creación de la UUID de la sesión
        session_uuid = self._generate_session_uuid()
        # Creación del registro en la base de datos
        self._create_user_session(
            user_id,
            session_uuid,
            expiration_date,
        )

        return ( session_uuid, expiration_date )

    def is_active_user(
        self,
        session_uid: str,
    ) -> bool:

        # Obtención del valor de usuario activo
        is_active = self._compiler.is_active_user_from_session_uuid(session_uid)

        return is_active

    def _generate_token_expiration_date(
        self,
    ) -> datetime:

        # Generación de fecha de expiración
        expiration_date = datetime.now() + timedelta(**SESSION.EXPIRATION_TIME)

        return expiration_date

    def _generate_session_uuid(
        self,
    ) -> str:

        # Generación de la UUID
        generated_uuid = str( uuid4() )

        return generated_uuid

    def _create_user_session(
        self,
        user_id: int,
        session_uuid: str,
        expiration_date: datetime,
    ) -> None:

        # Creación de los datos
        data_to_insert = {
            FIELD_NAME.NAME: session_uuid,
            FIELD_NAME.USER_ID: user_id,
            'expiration_date': str(expiration_date),
            FIELD_NAME.CREATE_UID: 1,
            FIELD_NAME.WRITE_UID: 1,
        }

        # Se crean los datos en la base de datos
        self._dml.create(
            MODEL_NAME.BASE_USERS_SESSION,
            [data_to_insert,],
        )

    def get_session_uuid_user_id(
        self,
        session_uuid: str,
    ) -> int:

        # Obtención de la ID de la sesión del usuario
        [ session_id ] = self._main.search(
            ROOT_ID,
            MODEL_NAME.BASE_USERS_SESSION,
            [('name', '=', session_uuid)],
        )

        # Obtención de la ID de usuario
        user_id: int = self._main.get_value(
            ROOT_ID,
            MODEL_NAME.BASE_USERS_SESSION,
            session_id,
            'user_id',
        )

        return user_id
