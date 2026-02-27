import os
from ...._module_types import CredentialsFromEnv
from ...._settings import ENV_VARIABLE_NAME
from ...._core.modules._connection import Connection_Core
from ...._core.submods.connection import _Env_Interface

class _Env(_Env_Interface):
    _connection: Connection_Core

    def __init__(
        self,
    ) -> None:

        # Obtención de los nombres de variables de entorno
        host= ENV_VARIABLE_NAME.DATABASE.HOST
        port= ENV_VARIABLE_NAME.DATABASE.PORT
        db_name= ENV_VARIABLE_NAME.DATABASE.DB_NAME
        user= ENV_VARIABLE_NAME.DATABASE.USER
        password= ENV_VARIABLE_NAME.DATABASE.PASSWORD

        # Se inicializa el objeto de credenciales obteniendo los valores de variables de entorno
        self.credentials = CredentialsFromEnv(
            host= os.environ.get(host),
            port= os.environ.get(port),
            db_name= os.environ.get(db_name),
            user= os.environ.get(user),
            password= os.environ.get(password),
        )
