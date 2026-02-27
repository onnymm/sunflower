from typing import TypedDict
from .._base_categories._literals import (
    AutomationMethodName,
    ExecutionMethod,
    ModelName,
    SubmoduleName,
    WriteTransactionName,
)
from .._base_categories._filter import CriteriaStructure

class AutomationData(TypedDict):
    """
    #### Datos de registro de automatización
    Estructura de diccionario de datos.
    >>> {
    >>>     # Nombre de submódulo de Lylac
    >>>     'submodule': '_automations',
    >>>     # Función
    >>>     'callback': 'some_automation',
    >>>     # Nombre de modelo
    >>>     'model': 'base.model',
    >>>     # Transación de base de datos
    >>>     'transaction': 'create',
    >>>     # Estructura de criterio de búsqueda
    >>>     'criteria': [('state', '!=', 'base')],
    >>>     # Lista de campos
    >>>     'fields': ['name', 'model'],
    >>>     # Método de automatización
    >>>     'method': 'record',
    >>> }
    """
    submodule: SubmoduleName
    """
    #### Nombre de submódulo de Lylac
    Tipo de dato usado para apuntar hacia algún submódulo de la librería.

    Valores disponibles:
    - `'_automations'`: Módulo de automatizaciones
    - `'_ddl'`: Módulo de definición de datos de la base de datos.
    - `'_strc'`: Módulo de la estructura de la base de datos.
    - `'_validations'`: Módulo de validaciones.
    """
    callback: str
    """
    #### Función
    Nombre de función a ser ejecutada.
    """
    model: ModelName
    """
    #### Nombre de modelo
    Nombre de modelo base de la base de datos.

    Nombres disponibles:
    - `'base.model'`: Modelos
    - `'base.model.field'`: Campos
    - `'base.model.field.selection'`: Valores de selección
    - `'base.users'`: Usuarios

    También se puede utilizar un nombre personalizado si es que el modelo ya existe
    en la base de datos.
    """
    transaction: WriteTransactionName
    """
    #### Transación de base de datos
    Tipo de dato usado para especificación de transacción en la base de datos. Se
    omite el método `'select'` ya que no se utiliza para este tipado.
    - `'create'`: Método de creación en la base de datos
    - `'update'`: Método de modificación en la base de datos
    - `'delete'`: Método de eliminación en la base de datos
    """
    criteria: CriteriaStructure
    """
    ### Estructura de criterio de búsqueda
    La estructura del criterio de búsqueda consiste en una lista de dos tipos de
    dato:
    - `TripletStructure`: Estructura de tripletas para queries SQL
    - `LogicOperator`: Operador lógico

    Estas tuplas deben contenerse en una lista. En caso de haber más de una condición, se deben
    unir por operadores lógicos `'AND'` u `'OR'`. Siendo el operador lógico el que toma la
    primera posición:
    >>> ['&', ('amount', '>', 500), ('name', 'ilike', 'as')]
    >>> # "amount" es mayor a 500 y "name" contiene "as"
    >>> ['|', ('id', '=', 5), ('state', '=', 'posted')]
    >>> # "id" es igual a 5 o "state" es igual a "posted"

    ----
    #### Operador lógico
    Tipo de dato que representa un operador lógico.

    Los operadores lógicos disponibles son:
    - `'&'`: AND
    - `'|'`: OR

    ----
    #### Estructura de tripletas para queries SQL
    Este tipo de dato representa una condición sencilla para usarse en una
    transacción en base de datos.

    La estructura de una tripleta consiste en 3 diferentes parámetros:
    1. Nombre del campo del modelo
    2. Operador de comparación
    3. Valor de comparación

    Algunos ejemplos de tripletas son:
    >>> ('name', '=', 'Onnymm')
    >>> # Nombre es igual a "Onnymm"
    >>> ('id', '=', 5)
    >>> # ID es igual a 5
    >>> ('amount', '>', 500)
    >>> # "amount" es mayor a 500
    >>> ('name', 'ilike', 'as')
    >>> # "name" contiene "as"
    """
    fields: list[str]
    """
    #### Lista de campos
    Lista de campos correspondientes al modelo especificado.
    """
    method: AutomationMethodName
    """
    #### Método de automatización
    Tipo de dato usado para especificar el método de automatización que una
    función de automatización va a utilizar.
    - `'record'`: Automatización por registro.
    - `'list'`: Automatización por lista de registros.
    """

class ValidationData(TypedDict):
    """
    #### Datos de registro de validación
    Estructura de diccionario de datos.
    >>> {
    >>>     # Nombre de submódulo de Lylac
    >>>     'submodule': '_validations',
    >>>     # Función
    >>>     'callback': 'some_validation',
    >>>     # Nombre de modelo
    >>>     'model': 'base.model',
    >>>     # Transación de base de datos
    >>>     'transaction': 'create',
    >>>     # Método de validación
    >>>     'method': 'record',
    >>>     # Mensaje de error
    >>>     'message': 'El valor {value} no cumple con el formato esperado.'
    >>> }
    """
    submodule: SubmoduleName
    """
    #### Nombre de submódulo de Lylac
    Tipo de dato usado para apuntar hacia algún submódulo de la librería.

    Valores disponibles:
    - `'_automations'`: Módulo de automatizaciones
    - `'_ddl'`: Módulo de definición de datos de la base de datos.
    - `'_strc'`: Módulo de la estructura de la base de datos.
    - `'_validations'`: Módulo de validaciones.
    """
    callback: str
    """
    #### Función
    Nombre de función a ser ejecutada.
    """
    model: ModelName
    """
    #### Nombre de modelo
    Nombre de modelo base de la base de datos.

    Nombres disponibles:
    - `'base.model'`: Modelos
    - `'base.model.field'`: Campos
    - `'base.model.field.selection'`: Valores de selección
    - `'base.users'`: Usuarios

    También se puede utilizar un nombre personalizado si es que el modelo ya existe
    en la base de datos.
    """
    transaction: WriteTransactionName
    """
    #### Transación de base de datos
    Tipo de dato usado para especificación de transacción en la base de datos. Se
    omite el método `'select'` ya que no se utiliza para este tipado.
    - `'create'`: Método de creación en la base de datos
    - `'update'`: Método de modificación en la base de datos
    - `'delete'`: Método de eliminación en la base de datos
    """
    method: ExecutionMethod
    """
    #### Método de validación
    Tipo de dato usado para especificar el método de validación que una
    función de validación va a utilizar.
    - `'record'`: Validación por registro.
    - `'list'`: Validación por lista de registros.
    """
    message: str
    """
    #### Mensaje de error
    Mensaje a mostrar cuando una validación falla.
    """
