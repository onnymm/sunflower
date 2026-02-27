from typing import Generic
from pydantic import BaseModel
from .._base_categories import _T
from ._base import (
    _HasAutomationMethod,
    _HasCallbackName,
    _HasCriteriaStructure,
    _HasFields,
    _HasModelName,
    _HasSubmodule,
    _HasTransaction,
)

class AutomationModel(
    _HasSubmodule,
    _HasCallbackName,
    _HasModelName,
    _HasTransaction,
    _HasCriteriaStructure,
    _HasFields,
    _HasAutomationMethod,
):
    """
    #### Automatización
    Modelo de datos de automatización.
    >>> class AutomationModel(BaseModel):
    >>>     # Nombre de submódulo de Lylac
    >>>     submodule: Submodule
    >>>     # Función
    >>>     callback: str
    >>>     # Nombre de modelo
    >>>     model: ModelName
    >>>     # Transación de base de datos
    >>>     transaction: Transaction
    >>>     # Estructura de criterio de búsqueda
    >>>     criteria: CriteriaStructure
    >>>     # Lista de campos
    >>>     fields: list[str]
    >>>     # Método de automatización
    >>>     method: AutomationMethod
    """
    ...

class DataPerRecord(BaseModel, Generic[_T]):
    """
    #### Datos por registro
    Tipado usado para argumento de entrada de funciones que se usan como
    automatizaciones. Este tipo de dato está incompleto y requiere tener
    especificado un tipo de registro. De esta manera se puede mejorar la
    programación de la automatización.
    >>> class DataPerRecord(BaseModel, _T):
    >>>     # ID
    >>>     id: int
    >>>     # Datos del registro
    >>>     record_data: _T

    Uso:
    >>> def my_automation(
    >>>     params: DataPerRecord[ModelRecord.BaseModel],
    >>> ) -> None:
    >>>     # Se procesa el registro
    >>>     ...

    ----

    #### Tipo de dato genérico
    Tipo de dato genérico usado para declarar entradas y salidas dinámicas en
    funciones:
    >>> def do_something(param: _T) -> _T:
    >>>     ...
    >>> a = do_something(5) # `a` se tipa como entero
    >>> b = do_something('Onnymm') # `b` se tipa como cadena de texto
    >>> c = do_something(True) # `c` se tipa como booleano

    Este tipo de dato también se puede usar para transformación de tipos de dato de
    entradas y salidas:
    >>> def get_first_item(iterable_object: list[_T]) -> _T:
    >>>     return iterable_object[0]
    >>> 
    >>> a = get_first_item([1, 2, 3]) # `a` se tipa como entero
    >>> b = get_first_item(['uno', 'dos', 'tres']) # `b` se tipa como cadena de texto
    >>> c = get_first_item([True, False]) # `c` se tipa como booleano
    """
    id: int
    """
    #### ID
    ID del registro.
    """
    record_data: _T
    """
    #### Datos del registro
    Datos del registro en la base de datos.
    """

class DataPerTransaction(BaseModel, Generic[_T]):
    """
    #### Datos por transacción
    Tipado usado para argumento de entrada de funciones que se usan como
    automatizaciones. Este tipo de dato está incompleto y requiere tener
    especificado un tipo de registro. De esta manera se puede mejorar la
    programación de la automatización.
    >>> class DataPerTransaction(BaseModel, _T):
    >>>     # IDs
    >>>     ids: list[int]
    >>>     # Datos de los registros
    >>>     record_data: list[_T]

    Uso:
    >>> def my_automation(
    >>>     params: DataPerTransaction[ModelRecord.BaseModel_],
    >>> ) -> None:
    >>>     # Se procesan los registros
    >>>     ...

    ----

    #### Tipo de dato genérico
    Tipo de dato genérico usado para declarar entradas y salidas dinámicas en
    funciones:
    >>> def do_something(param: _T) -> _T:
    >>>     ...
    >>> a = do_something(5) # `a` se tipa como entero
    >>> b = do_something('Onnymm') # `b` se tipa como cadena de texto
    >>> c = do_something(True) # `c` se tipa como booleano

    Este tipo de dato también se puede usar para transformación de tipos de dato de
    entradas y salidas:
    >>> def get_first_item(iterable_object: list[_T]) -> _T:
    >>>     return iterable_object[0]
    >>> 
    >>> a = get_first_item([1, 2, 3]) # `a` se tipa como entero
    >>> b = get_first_item(['uno', 'dos', 'tres']) # `b` se tipa como cadena de texto
    >>> c = get_first_item([True, False]) # `c` se tipa como booleano

    """
    ids: list[int]
    """
    #### IDs
    Lista de IDs de los registros.
    """
    records_data: list[_T]
    """
    #### Datos de los registros
    Datos de los registros en la base de datos.
    """
