from typing import Callable
from ._base_categories import RecordIDs
from ._models import (
    DataPerRecord,
    DataPerTransaction,
)

AutomationTemplate = Callable[[DataPerRecord | DataPerTransaction], None]
"""
### Función de automatización
Estructura que debe tener una función para registrarse como automatización.
>>> def some_automation(params: DataPerRecord[Any]) -> None:
>>>     ...
"""

PosCreationCallback = Callable[[RecordIDs], None]
"""
### Función poscreación
Función que recibe una lista de IDs y hace algo con ellas.

>>> def some_callback(params: list[int]) -> None:
>>>     ...
"""

PosUpdateCallback = Callable[[], None]
"""
### Función posactualización
Función que se ejecuta después de la actualización de registros

>>> def some_callback(params: list[int]) -> None:
>>>     ...
"""

Many2ManyUpdatesOnCreateCallback = Callable[[RecordIDs], None]
"""
### Actualización de registros `many2many` en creación
Función que ejecuta una subtransacción de registros referenciados tras la
creación de registros que los referencían.
"""

Many2ManyUpdatesOnUpdateCallback = Callable[[], None]
"""
### Actualización de registros `many2many` en actualización
FUnción que ejecuta una subtransacción de registros referenciados tras la
modificación de registros que los referencían.
"""
