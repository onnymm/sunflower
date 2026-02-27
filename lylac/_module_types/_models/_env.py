from pydantic import (
    BaseModel,
    field_validator,
)
from urllib.parse import quote

class CredentialsFromEnv(BaseModel):
    """
    ## Credenciales de la base de datos
    Objeto contenedor de los valores de credenciales para conexión con la base de
    datos.
    >>> class Credentials(BaseModel):
    >>>     # Dirección URL en donde se aloja la base de datos.
    >>>     host: str
    >>>     # Puerto del host en donde se aloja la base de datos.
    >>>     port: str
    >>>     # Nombre de la base de datos.
    >>>     db_name: str
    >>>     # Nombre de usuario de acceso a la base de datos.
    >>>     user: str
    >>>     # Contraseña de acceso a la base de datos.
    >>>     password: str
    """
    host: str
    """
    Dirección URL en donde se aloja la base de datos.
    """
    port: int
    """
    Puerto del host en donde se aloja la base de datos.
    """
    db_name: str
    """
    Nombre de la base de datos.
    """
    user: str
    """
    Nombre de usuario de acceso a la base de datos.
    """
    password: str
    """
    Contraseña de acceso a la base de datos.
    """

    @field_validator('password')
    def _encode(cls, value: str) -> str:
        return quote(value)
