from typing import (
    Any,
    Callable,
    Generic,
    TypedDict,
)
from pydantic import BaseModel
from ...._module_types import (
    _T,
    RecordData,
    ExecutionMethod,
)

class _BaseValidationOnCreateArgs(BaseModel):

    model_name: str
    """Nombre del modelo."""
    model_id: int
    """ID del modelo."""

# Argumentos de entrada de función de validación
class _ValidationOnCreateArgs(_BaseValidationOnCreateArgs, Generic[_T]):
    data: _T
    """Datos del o los registros."""
class _ValidationOnCreateArgs_Group(_BaseValidationOnCreateArgs, Generic[_T]):
    data: list[_T]
    """Datos del o los registros."""
class _ValidationOnCreateArgs_Mixed(_BaseValidationOnCreateArgs, Generic[_T]):
    data: _T | list[_T]
    """Datos del o los registros."""

class _ValidationOnCreateParams(TypedDict, Generic[_T]):

    callback: _T
    """Función de validación en la creación de registros."""
    method: ExecutionMethod
    """
    Método de ejecución de validación.
    >>> Literal['record', 'list']
    """
    message: str
    """Mensaje de error arrojado si los datos evaluados no son válidos."""

# Tipado de funciones
_IndividualValidationOnCreateCallback = Callable[[ _ValidationOnCreateArgs ], Any]
_GroupValidationOnCreateCallback = Callable[[ _ValidationOnCreateArgs_Group ], Any]

class _BaseValidationOnUpdateArgs(BaseModel, Generic[_T]):
    model_name: str
    """Nombre del modelo."""
    model_id: int
    """ID del modelo."""

# Argumentos de entrada de función de validación
class _ValidationOnUpdateArgs(_BaseValidationOnUpdateArgs, Generic[_T]):
    record_ids: int
    """IDs de los registros."""
    data: _T
    """Datos de los registros."""
class _ValidationOnUpdateArgs_Group(_BaseValidationOnUpdateArgs, Generic[_T]):
    record_ids: list[int]
    """IDs de los registros."""
    data: _T
    """Datos de los registros."""
class _ValidationOnUpdateArgs_Mixed(_BaseValidationOnUpdateArgs, Generic[_T]):
    record_ids: int | list[int]
    """IDs de los registros."""
    data: _T
    """Datos de los registros."""

class _ValidationOnUpdateParams(TypedDict, Generic[_T]):

    callback: _T
    """Función de validación en la creación de registros."""
    method: ExecutionMethod
    """
    Método de ejecución de validación.
    >>> Literal['record', 'list']
    """
    message: str
    """Mensaje de error arrojado si los datos evaluados no son válidos."""

# Tipado de funciones
_IndividualValidationOnUpdateCallback = Callable[[ _ValidationOnUpdateArgs ], Any]
_GroupValidationOnUpdateCallback = Callable[[ _ValidationOnUpdateArgs_Group ], Any]

class Validation():

    class Create():

        class Mixed():

            Callback = _IndividualValidationOnCreateCallback | _GroupValidationOnCreateCallback
            """
            ### Función de validación
            Función de validación en creación de nuevos registros.
            >>> def some_validation(
            >>>     params: Validation.Create.Mixed.Args[...],
            >>> ) -> Any:
            >>>     ...
            """
            Args = _ValidationOnCreateArgs_Mixed
            """
            ### Argumentos de entrada de validación
            Argumentos de entrada de función de validación en creación de nuevos registros.
            >>> class _ValidationOnCreateArgs(BaseModel, _T):
            >>>     model_name: str
            >>>     model_id: int
            >>>     data: _T
            """
            Params = _ValidationOnCreateParams[Callback]
            """
            ### Parámetros de validación de creación
            Parámetros que definen una función de validación, su método de ejecución y el
            mensaje de error arrojado si los datos evaluados no son válidos.
            >>> class _ValidationOnCreateParams(BaseModel):
            >>>     # Función de validación en la creación de registros.
            >>>     callback: Validation.Create.Mixed.Callback
            >>>     # Método de ejecución de validación.
            >>>     method: ExecutionMethod
            >>>     # Mensaje de error arrojado si los datos evaluados no son válidos.
            >>>     message: str
            """

        class Individual():

            Callback = _IndividualValidationOnCreateCallback
            """
            ### Función de validación
            Función de validación en creación de un nuevo registro.
            >>> def some_validation(
            >>>     params: Validation.Create.Individual.Args[...],
            >>> ) -> Any:
            >>>     ...
            """
            Args = _ValidationOnCreateArgs
            """
            ### Argumentos de entrada de validación
            Argumentos de entrada de función de validación individual en creación de un
            nuevo registro.
            >>> class _ValidationOnCreateArgs(BaseModel, _T):
            >>>     model_name: str
            >>>     model_id: int
            >>>     data: _T
            """
            Params = _ValidationOnCreateArgs[Callback]
            """
            ### Parámetros de validación de creación individual
            Parámetros que definen una función de validación, su método de ejecución y el
            mensaje de error arrojado si los datos evaluados no son válidos.
            >>> class _ValidationOnCreateParams(BaseModel):
            >>>     # Función de validación en la creación de registros.
            >>>     callback: Validation.Create.Individual.Callback
            >>>     # Método de ejecución de validación.
            >>>     method = 'record'
            >>>     # Mensaje de error arrojado si los datos evaluados no son válidos.
            >>>     message: str
            """

        class Group():

            Callback = _GroupValidationOnCreateCallback
            """
            ### Función de validación
            Función de validación en creación de nuevos registros.
            >>> def some_validation(
            >>>     params: Validation.Create.Group.Args[...],
            >>> ) -> Any:
            >>>     ...
            """
            Args = _ValidationOnCreateArgs_Group
            """
            ### Argumentos de entrada de validación
            Argumentos de entrada de función de validación grupal en creación de nuevos registros.
            >>> class _ValidationOnCreateArgs(BaseModel, _T):
            >>>     model_name: str
            >>>     model_id: int
            >>>     data: _T
            """
            Params = _ValidationOnCreateArgs[Callback]
            """
            ### Parámetros de validación de creación individual
            Parámetros que definen una función de validación, su método de ejecución y el
            mensaje de error arrojado si los datos evaluados no son válidos.
            >>> class _ValidationOnCreateParams(BaseModel):
            >>>     # Función de validación en la creación de registros.
            >>>     callback: Validation.Create.Group.Callback
            >>>     # Método de ejecución de validación.
            >>>     method: 'list'
            >>>     # Mensaje de error arrojado si los datos evaluados no son válidos.
            >>>     message: str
            """

    class Update():

        class Mixed():

            Callback = _IndividualValidationOnUpdateCallback | _GroupValidationOnUpdateCallback
            """
            ### Función de validación
            Función de validación en modificación de registros.
            >>> def some_validation(
            >>>     params: Validation.Update.Mixed.Args[...],
            >>> ) -> Any:
            >>>     ...
            """
            Args = _ValidationOnUpdateArgs_Mixed
            """
            ### Argumentos de entrada de validación
            Argumentos de entrada de función de validación en modificación de registros.
            >>> class _ValidationOnUpdateArgs(BaseModel, _T):
            >>>     model_name: str
            >>>     model_id: int
            >>>     record_ids: int | list[int]
            >>>     data: _T
            """
            Params = _ValidationOnUpdateParams[Callback]
            """
            ### Parámetros de validación de modificación grupal o individual
            Parámetros que definen una función de validación, su método de ejecución y el
            mensaje de error arrojado si los datos evaluados no son válidos.
            >>> class _ValidationOnUpdateParams(TypedDict):
            >>>     # Función de validación en la modificación de registros.
            >>>     callback: Validation.Update.Mixed.Callback
            >>>     # Método de ejecución de validación.
            >>>     method: 'list'
            >>>     # Mensaje de error arrojado si los datos evaluados no son válidos.
            >>>     message: str
            """

        class Individual():

            Callback = _IndividualValidationOnUpdateCallback
            """
            ### Función de validación
            Función de validación en modificación de un registro.
            >>> def some_validation(
            >>>     params: Validation.Update.Individual.Args[...],
            >>> ) -> Any:
            >>>     ...
            """
            Args = _ValidationOnUpdateArgs
            """
            ### Argumentos de entrada de validación
            Argumentos de entrada de función de validación en modificación de un registro.
            >>> class _ValidationOnUpdateArgs(BaseModel, _T):
            >>>     model_name: str
            >>>     model_id: int
            >>>     record_ids: int
            >>>     data: _T
            """
            Params = _ValidationOnUpdateParams[Callback]
            """
            ### Parámetros de validación de modificación grupal
            Parámetros que definen una función de validación, su método de ejecución y el
            mensaje de error arrojado si los datos evaluados no son válidos.
            >>> class _ValidationOnUpdateParams(TypedDict):
            >>>     # Función de validación en la modificación de un registro.
            >>>     callback: Validation.Update.Group.Callback
            >>>     # Método de ejecución de validación.
            >>>     method: 'list'
            >>>     # Mensaje de error arrojado si los datos evaluados no son válidos.
            >>>     message: str
            """

        class Group():

            Callback = _GroupValidationOnUpdateCallback
            """
            ### Función de validación
            Función de validación en modificación de registros.
            >>> def some_validation(
            >>>     params: Validation.Update.Group.Args[...],
            >>> ) -> Any:
            >>>     ...
            """
            Args = _ValidationOnUpdateArgs_Group
            """
            ### Argumentos de entrada de validación
            Argumentos de entrada de función de validación en modificación de registros.
            >>> class _ValidationOnCreateArgs(BaseModel, _T):
            >>>     model_name: str
            >>>     model_id: int
            >>>     record_ids: list[int]
            >>>     data: _T
            """
            Params = _ValidationOnUpdateParams[Callback]
            """
            ### Parámetros de validación de modificación individual
            Parámetros que definen una función de validación, su método de ejecución y el
            mensaje de error arrojado si los datos evaluados no son válidos.
            >>> class _ValidationOnUpdateParams(TypedDict):
            >>>     # Función de validación en la modificación de registros.
            >>>     callback: Validation.Update.Group.Callback
            >>>     # Método de ejecución de validación.
            >>>     method: 'list'
            >>>     # Mensaje de error arrojado si los datos evaluados no son válidos.
            >>>     message: str
            """

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
