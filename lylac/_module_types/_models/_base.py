from pydantic import BaseModel
from .._base_categories import (
    CriteriaStructure,
    AutomationMethodName,
    SubmoduleName,
    WriteTransactionName,
)

class _HasSubmodule(BaseModel):
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

class _HasCallbackName(BaseModel):
    callback: str
    """
    #### Función
    Nombre de función a ser ejecutada.
    """

class _HasModelName(BaseModel):
    model: str
    """
    #### Nombre de modelo
    Nombre de modelo base de la base de datos.

    Nombres disponibles:
    - `'base.model'`: Modelos
    - `'base.model.field'`: Campos
    - `'base.model.field.selection'`: Valores de selección
    - `'base.users'`: Usuarios
    """

class _HasTransaction(BaseModel):
    transaction: WriteTransactionName
    """
    #### Transación de base de datos
    Tipo de dato usado para especificación de transacción en la base de datos. Se
    omite el método `'select'` ya que no se utiliza para este tipado.
    - `'create'`: Método de creación en la base de datos
    - `'update'`: Método de modificación en la base de datos
    - `'delete'`: Método de eliminación en la base de datos
    """

class _HasCriteriaStructure(BaseModel):
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

class _HasFields(BaseModel):
    fields: list[str]
    """
    #### Lista de campos
    Lista de campos correspondientes al modelo especificado.
    """

class _HasAutomationMethod(BaseModel):
    method: AutomationMethodName
    """
    #### Método de automatización
    Tipo de dato usado para especificar el método de automatización que una
    función de automatización va a utilizar.
    - `'record'`: Automatización por registro.
    - `'list'`: Automatización por lista de registros.
    """
