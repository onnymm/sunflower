from datetime import datetime
from typing import TypedDict
import jwt
from jwt import ExpiredSignatureError
from ...._constants import MESSAGES
from ...._core import ENV_VARIABLES
from ...._core.submods.auth import _Token_Interface
from ...._core.modules import Auth_Core
from ....errors import ExpiredSessionToken

class TokenData(TypedDict):
    uuid: str
    exp: datetime

class Token(_Token_Interface):
    _auth: Auth_Core

    def __init__(
        self,
        instance: Auth_Core,
    ) -> None:
        
        # Asignación de instancia propietaria
        self._auth = instance
        # Asignación de instancia principal
        self._main = instance._main

        # Algoritmo de encriptación
        self._algorithm = "HS256"
        # Clave de encriptación
        self._auth_key = ENV_VARIABLES.CRYPT.AUTH

    def create_session_token(
        self,
        session_uuid: str,
        expiration_date: datetime,
    ) -> str:

        # Construcción del diccionario a encriptar
        data_to_encode = {
            'uuid': session_uuid,
            'exp': expiration_date,
        }
        # Generación del token
        session_token = self._encode(data_to_encode)

        return session_token

    def _encode(
        self,
        data_to_encode: TokenData,
    ) -> str:

        # Encriptación de los datos
        session_token = jwt.encode(
            data_to_encode,
            self._auth_key,
            algorithm= self._algorithm,
        )

        return session_token

    def get_session_uuid_from_token(
        self,
        token: str,
    ) -> str:

        # Obtención del diccionario de datos desde el token
        token_data = self._decode(token)
        # Obtención de la UUID de la sesión
        session_uuid = token_data['uuid']

        return session_uuid

    def _decode(
        self,
        token: str,
    ) -> TokenData:

        # Intento de decodificación del token
        try:
            # Desencriptación del token
            token_data: TokenData = jwt.decode(
                token,
                self._auth_key,
                self._algorithm,
            )

            return token_data

        # Si el token expiró...
        except ExpiredSignatureError:
            # Se arroja el error de sesión expirada
            raise ExpiredSessionToken(MESSAGES.ACCESS.EXPIRED_TOKEN)
