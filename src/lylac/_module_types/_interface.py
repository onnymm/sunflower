from typing import Union
import pandas as pd
from ._base import RecordValue
from ._dicts import CredentialsArgs

# Tipo de dato retornado por métodos de lectura en el módulo principal
DataOutput = Union[pd.DataFrame | dict[str, RecordValue]]
"""
### Tipo de dato retornado
Tipo de dato retornado por métodos de lectura en el módulo principal.
>>> Union[pd.DataFrame | dict[str, RecordValue]]
"""

# Formato de credenciales para conexión a base de datos
CredentialsAlike = Union[CredentialsArgs, str, None]
"""
## Credenciales de acceso a la base de datos
Diccionario contenedor de los valores de credenciales para conectar o URL de
conexión con la base de datos.

Uso:
>>> # Formato de diccionario
>>> {
>>>     'host': 'https://www.db_host.com',
>>>     'port': 5432,
>>>     'db_name': 'my_database',
>>>     'user': 'postgresql',
>>>     'password': 'somepassword123'
>>> }
>>> # Formato de URL
>>> f"postgresql+psycopg2://postgres:{password}@{host}:{port}/{database_name}"
"""

FieldAlias = tuple[str, str]
"""
### Alias de campo
Uso de alias en la invocación de un campo.

Uso:
>>> ('field_id.model_id.name', 'model_name')
"""

ModelField = Union[str, FieldAlias]
"""
### Campo de modelo
Declaración de uso de un campo de modelo
"""
