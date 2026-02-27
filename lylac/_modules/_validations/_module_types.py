from typing import (
    Any,
    TypedDict,
)
from ..._module_types import (
    RecordData,
    Validation,
)

class _ValidationsPerTransaction(TypedDict):
    create: list[Validation.Create.Mixed.Params]

# Núcleo de validaciones
ValidationsHub = dict[str, _ValidationsPerTransaction]

# Mensajes a mostrar
class ErrorToShow(TypedDict):
    """
    ### Error a mostrar en validación fallida
    Error a mostrar una cuando una validación arroja datos que no cumplen con ésta.
    >>> {
    >>>     'value': ...,
    >>>     'message': '...',
    >>>     'data': {...}
    >>> }
    """
    value: Any
    """Datos que no cumplen con la validación."""
    message: str
    """Mensage que indica la razón de la validación fallida."""
    data: RecordData | list[RecordData]
    """Datos del o los objetos que no cumplieron con la validación."""
