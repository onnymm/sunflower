from typing import (
    Callable,
    Literal,
)
from pydantic import BaseModel
from ..._module_types import (
    CriteriaStructure,
    WriteTransactionName,
)
from ..._contexts import AutomationCallback

# Estructura de datos de automatización programada
class ProgrammedAutomation(BaseModel):
    """
    #### Automatización programada
    Este diccionario contiene una condición de filtro para dictar en qué casos la
    automatización debe ser ejecutada únicamente.

    Ejemplo:
    >>> {
    >>>     # Condición que dicta en qué casos se ejecuta la automatización
    >>>     'criteria': [('active', '=', True)],
    >>>     # Función de automatización
    >>>     'callback': do_something,
    >>>     # Campos a leer
    >>>     'fields': ['name', 'create_uid'],
    >>>     # Tipo de ejecución
    >>>     'execution': 'record',
    >>> }

    #### `criteria`
    Condición que dicta en qué casos se ejecuta la automatización.
    >>> [('active', '=', True)]

    #### `callback`
    Función utilizada para ejecutar una automación.
    >>> def automation_do_something(record_ids: list[int]) -> None:
    >>>     # do something

    #### `fields`
    Lista de nombres de campo del modelo del registro a leer. Esto facilita la
    construcción de la automatización ahorrando la búsqueda y extracción de valores
    del o los registros y anticipando la extracción de valores de un registro a ser
    eliminado y ser usados posteriormente por la automatización cuando los datos
    del registro ya no existen pero son requeridos.
    #### `execution`
    Tipo de ejecución de la automatización. Si la automatización se declara con
    ejecución por registro, la función para automatización provista recibirá los
    datos de un registro individual en forma de diccionario e, internamente, se
    ejecutará esta función por cada registro. Si la automatización se declara por
    todos los registros se pueden realizar cálculos en conjunto y/o realizar
    iteraciones por cada uno de los diccionarios que contienen los datos
    actualizados de los registros. La función recibe, en este caso, una lista de
    diccionarios, cada uno con los datos actualizados de cada registro.
    """
    criteria: CriteriaStructure
    """Condición que dicta en qué casos se ejecuta la automatización."""
    callback: AutomationCallback
    """
    ### Función de automatización
    Estructura que debe tener una función para registrarse como automatización.
    >>> # Automatización de ejecución por registro individual
    >>> def some_automation(ctx: Context.Individual[...]) -> None:
    >>>     ...
    >>> # Automatización de ejecución por lista de registros
    >>> def some_automation(ctx: Context.Group[...]) -> None:
    >>>     ...
    """
    fields: list[str]
    """
    #### Campos a leer
    Lista de nombres de campo del modelo del registro a leer. Esto facilita la
    construcción de la automatización ahorrando la búsqueda y extracción de valores
    del o los registros y anticipando la extracción de valores de un registro a ser
    eliminado y ser usados posteriormente por la automatización cuando los datos
    del registro ya no existen pero son requeridos.
    """
    execution: Literal['record', 'all']
    """
    #### Tipo de ejecución
    Tipo de ejecución de la automatización. Si la automatización se declara con
    ejecución por registro, la función para automatización provista recibirá los
    datos de un registro individual en forma de diccionario e, internamente, se
    ejecutará esta función por cada registro. Si la automatización se declara por
    todos los registros se pueden realizar cálculos en conjunto y/o realizar
    iteraciones por cada uno de los diccionarios que contienen los datos
    actualizados de los registros. La función recibe, en este caso, una lista de
    diccionarios, cada uno con los datos actualizados de cada registro.
    """

# Desencadenantes de automatización divididos por tipo de transacción
TransactionProgAutoms = dict[WriteTransactionName, list[ProgrammedAutomation]]
"""
Diccionario que segmenta las automatizaciones por tipo de transacción en la
base de datos.
>>> {
>>>     'create': [
>>>         prog_autom_1,
>>>         prog_autom_2,
>>>         prog_autom_3,
>>>     ],
>>>     'delete': [
>>>         prog_autom_4,
>>>         prog_autom_5,
>>>     ],
>>> }

### Automatización programada
Este diccionario contiene una condición de filtro para dictar en qué casos la
automatización debe ser ejecutada únicamente.

Ejemplo:
>>> {
>>>     'criteria': [('active', '=', True)],
>>>     'callback': do_something, # Función
>>> }

#### `criteria`
Condición que dicta en qué casos se ejecuta la automatización.
>>> [('active', '=', True)]

#### `callback`
Función utilizada para ejecutar una automación.
>>> def automation_do_something(record_ids: list[int]) -> None:
>>>     # do something
"""

# Grupos de desencadenantes de automatización divididos por nombres de tabla
AutomationsHub = dict[str, TransactionProgAutoms]
"""
### Centro de automatizaciones
Colección de datos principal que almacena todas las automatizaciones
>>> hub: dict[str, TransactionProgAutoms] = {
>>>     'base.model': {
>>>         'create': [
>>>             prog_autom_1,
>>>             prog_autom_2,
>>>         ],
>>>         'delete': [...],
>>>     },
>>>     'base.model.field': {...},
>>> }
"""

CompiledModificationAutomation = Callable[[], None]
"""
#### Automatización de transacción de modificación compilada
Función de automatización creada a partir de las instrucciones provistas desde
el núcleo de automatizaciones y que contiene la lista de registros de la tabla
específica en dónde ejecutar las instrucciones provistas por la función
asociada a las instrucciones en los datos de la automatización, en la ejecución
de una transacción de modificación de datos, ya sea creación o actualización.
Esta función no recibe argumentos.
>>> def autom() -> None:
>>>     # Ejecución de instrucciones
>>>     ...
"""

CompiledDeletionAutomation = Callable[[list[int]], None]
"""
#### Automatización de transaccion de eliminación compilada
Función de automatización creada a partir de las instrucciones provistas desde
el núcleo de automatizaciones y que contiene la lista de registros de la tabla
específica en dónde ejecutar las instrucciones provistas por la función
asociada a las instrucciones en los datos de la automatización, en la ejecución
de una transacción de eliminación de datos, recibiendo como argumento la lista
de IDs de registros eliminados correctamente.
>>> def autom(deleted_ids: list[int]) -> None:
>>>     # Ejecución de las intrucciones
>>>     ...
"""
