import re
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.sql.selectable import Select, TypedReturnsRows
from ..._constants import MESSAGES
from ..._core.modules import Connection_Core
from ..._core.main import _Lylac_Core
from ...errors import URLFormatError, CredentialsError
from ..._module_types import (
    CredentialsArgs,
    CredentialsFromEnv,
    CredentialsAlike,
    _T,
)
from ._submodules import _Env

class Connection(Connection_Core):

    def __init__(
        self,
        instance: _Lylac_Core,
        credentials: CredentialsAlike,
    ) -> None:

        # Asignación de la instancia propietaria
        self._main = instance

        # Creación del motor de conexión a base de datos
        self._create_connection(credentials)

    def execute(
        self,
        statement: Select[_T] | TypedReturnsRows[_T],
        commit: bool = False
    ) -> CursorResult[_T]:

        # Conexión con la base de datos
        with self._main._engine.connect() as conn:
            # Ejecución en la base de datos
            response = conn.execute(statement)
            # Commit de los cambios
            if commit:
                conn.commit()

        # Retorno de respuesta tipada
        return response

    def _create_connection(
        self,
        credentials: CredentialsAlike,
    ) -> None:

        # Obtención de la URL de la base de datos
        url = self._get_database_url(credentials)
        # Creación del motor de conexión
        self._main._engine = self._create_engine(url)

    def _get_database_url(
        self,
        credentials: CredentialsAlike,
    ) -> str:

        # Si las credenciales provistas son una URL...
        if isinstance(credentials, str):
            # Validación del formato de la URL
            url = self._validate_url(credentials)

        # Si las credenciales provistas son un diccionario...
        elif isinstance(credentials, dict):
            # Obtención de las credenciales
            url = self._build_database_url(credentials)

        # Si no hay credenciales provistas...
        elif credentials is None:
            # Se toman las credenciales desde las variables de entorno
            url = self._get_credentials_from_env()

        # Si las credenciales están en un formato distinto...
        else:
            # Se lanza error de tipo de dato
            raise CredentialsError(MESSAGES.DATA_FORMAT.WRONG_CREDENTIALS_TYPE)

        return url

    def _build_database_url(
        self,
        credentials: CredentialsArgs,
    ) -> str:

        # Obtención de las credenciales desde un diccionario provisto
        credentials = CredentialsFromEnv(**credentials)
        # Validación de la URL construida
        url = self._build_url(credentials)

        return url

    def _get_credentials_from_env(
        self,
    ) -> str:

        # Obtención de las variables de entorno
        credentials = _Env().credentials
        # Validación de la URL construida
        url = self._build_url(credentials)

        return url

    def _build_url(
        self,
        credentials: CredentialsFromEnv,
    ) -> str:

        # Obtención de los parámetros a utilizar
        host = credentials.host
        port = credentials.port
        db_name = credentials.db_name
        user = credentials.user
        password = credentials.password

        # Construcción de la URL
        built_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
        # Validación de la URL
        url = self._validate_url(built_url)

        return url

    def _validate_url(
        self,
        url: str,
    ) -> str:

        # Patrón de estructura de texto que debe cumplir la URL provista
        pattern = r'postgresql\+psycopg2://postgres:.*@[a-zA-Z\d\-]*:\d{4}/.*'

        # Si la URL no cumple con el formato...
        if re.match(pattern, url) is None:
            # Se arroja un error
            raise URLFormatError(MESSAGES.DATA_FORMAT.ENGINE_URL_ERROR)
        # Si el formato se cumple se retorna la URL
        else:
            return url

    def _create_engine(
        self,
        url: str,
    ) -> Engine:

        # Creación del motor de conexión con la base de datos
        engine = create_engine(url)

        return engine
