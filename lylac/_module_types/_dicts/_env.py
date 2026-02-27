from typing import TypedDict

class CredentialsArgs(TypedDict):
    """
    ## Credenciales de la base de datos
    Diccionario contenedor de los valores de credenciales para conexión con la base
    de datos.
    >>> {
    >>>     'host': 'https://www.db_host.com',
    >>>     'port': 5432,
    >>>     'db_name': 'my_database',
    >>>     'user': 'postgresql',
    >>>     'password': 'somepassword123'
    >>> }
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
