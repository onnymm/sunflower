# lylac
Gestor de conexión a bases de datos altamente personalizable.

Instalación:
```bash
pip install git+https://github.com/onnymm/lylac.git
```

## *Índice*

## [TIPADOS](#tipados-1)

### **[[Tipados base](#tipados-base-1)]**

**[Base](#base)**
- [`RecordValue` Valor de registro](#recordvalue-valor-de-registro)
- [`RecordData` Datos de registro](#recorddata-datos-de-registro)

### **[[Tipados principales](#tipados-principales-1)]**

**[Genéricos](#genéricos)**
- [`_T` Tipo de dato genérico](#_t-tipo-de-dato-genérico)

**[Filtros](#filtros)**
- [`ComparisonOperator` Operador de comparación](#comparisonoperator-operador-de-comparación)
- [ `LogicOperator` Operador lógico](#logicoperator-operador-lógico)
- [`TripletStructure` Estructura de tripletas para queries SQL](#tripletstructure-estructura-de-tripletas-para-queries-sql)
- [`CriteriaStructure` Estructura de criterio de búsqueda](#criteriastructure-estructura-de-criterio-de-búsqueda)

**[Literales](#literales)**
- [`ExecutionMethod` Método de ejecución](#executionmethod-método-de-validación)
- [`ModelName` Nombre de modelo](#modelname-nombre-de-modelo)
- [`ModificationTransaction` Transacción de modificación](#modificationtransaction-transacción-de-modificación)
- [`Submodule` Nombre de submódulo de Lylac](#submodule-nombre-de-submódulo-de-lylac)
- [`Transaction` Transación de base de datos](#transaction-transación-de-base-de-datos)
- [`TType` Tipo de dato en campo de modelo en la base de datos](#ttype-tipo-de-dato-en-campo-de-modelo-en-la-base-de-datos)
- [`OutputOptions` Salida de datos](#outputoptions-salida-de-datos)

**[Modelos](#modelos)**
- [`DataBaseDataType` Tipo de dato de SQLAlchemy](#databasedatatype-tipo-de-dato-de-sqlalchemy)

### **[[Tipados de diccionarios](#tipados-de-diccionarios-1)]**

**[Diccionarios de datos](#diccionarios-de-datos)**

- [`AutomationData` Datos de registro de automatización](#automationdata-datos-de-registro-de-automatización)
- [`ValidationData` Datos de registro de validación](#validationdata-datos-de-registro-de-validación)

**[Diccionarios de credenciales](#diccionarios-de-credenciales)**

- [`CredentialsArgs` Credenciales de la base de datos](#credentialsargs-credenciales-de-la-base-de-datos)

**[Diccionarios de estructura de base de datos](#diccionarios-de-estructura-de-base-de-datos)**
- [`FieldProperties` Propiedades de campo](#fieldproperties-propiedades-de-campo)
- [`ModelMap` Mapa de atributos de modelo](#modelmap-mapa-de-atributos-de-modelo)

**[Diccionarios de registros](#diccionarios-de-registros)**
- [`NewRecord` Nuevo registro](#newrecord-nuevo-registro)
    - [`Model` Nuevo registro de modelo](#model-nuevo-registro-de-modelo)
    - [`ModelField` Nuevo registro de campo](#modelfield-nuevo-registro-de-campo)
    - [`ModelFieldSelection` Nuevo registro de selección de campo](#modelfieldselection-nuevo-registro-de-selección-de-campo)
    - [`User` Nuevo registro de usuario](#user-nuevo-registro-de-usuario)
- [`ModelRecordData` Datos de registros en la base de datos](#modelrecorddata-datos-de-registros-en-la-base-de-datos)
    - [`BaseModel_` Datos de modelo](#basemodel_-datos-de-modelo)
    - [`BaseModelField` Datos de campo](#basemodelfield-datos-de-campo)
    - [`BaseModelFieldSelection` Datos de valores de selección de campo](#basemodelfieldselection-datos-de-valores-de-selección-de-campo)
    - [`BaseUsers` Datos de usuario](#baseusers-datos-de-usuario)

### **[[Tipados de Modelos](#tipados-de-modelos-1)]**

**[Modelos de automatizaciones](#modelos-de-automatizaciones)**
- [`AutomationModel` Automatización](#automationmodel-automatización)
- [`DataPerRecord` Datos por registro](#dataperrecord-datos-por-registro)
- [`DataPerTransaction` Datos por transacción](#datapertransaction-datos-por-transacción)

**[Modelos de definiciones](#modelos-de-definiciones)**
- [`FieldDefinition` Definición de campo](#fielddefinition-definición-de-campo)

**[Modelos de credenciales](#modelos-de-credenciales)**
- [`CredentialsFromEnv` Credenciales de la base de datos](#credentialsfromenv-credenciales-de-la-base-de-datos)

### **[[Tipados de funciones](#tipados-de-funciones-1)]**

**[Funciones internas](#funciones-internas)**
- [`AutomationTemplate` Función de automatización](#automationtemplate-función-de-automatización)

### **[[Tipados complejos](#tipados-complejos-1)]**

**[Argumentos de funciones](#argumentos-de-funciones)**
- [`CredentialsAlike` Credenciales de acceso a la base de datos](#credentialsalike-credenciales-de-acceso-a-la-base-de-datos)

**[Retornos de funciones](#retornos-de-funciones)**
- [`DataOutput` Tipo de dato retornado](#dataoutput-tipo-de-dato-retornado)

----

# Tipados

## Tipados base

### Base

#### `RecordValue` Valor de registro
```py
RecordValue = Union[
    int,
    float,
    str,
    bool,
    list[int],
    list[float],
    list[str],
    list[bool],
]
```
Este tipo de dato representa los tipos de dato válidos para diversos argumentos de entrada en métodos del módulo así como en funcionamientos internos, retornos en JSON y validaciones.
```py
# Tipos de dato individuales
5
2.8
'nombre'
True
# Listas de tipos de dato
[1, 2, 3]
[1.0, 3.5, 20.56]
['name', 'char', 'active']
[False, True, True]
```

#### `RecordData` Datos de registro
```py
RecordData = dict[str, RecordValue]
```
Datos que contienen los valores de campo de un registro en la base de datos.
Ejemplo:
```py
{
    'name': 'Onnymm',
    'password': ...,
    'active': True,
}
```
> Para saber más sobre los tipos de datos usados consulta:
> - [`RecordValue` Valor de registro](#recordvalue-valor-de-registro)

----

## Tipados principales

### Genéricos

#### `_T` Tipo de dato genérico
```py
_T = TypeVar("_T")
```

Tipo de dato genérico usado para declarar entradas y salidas dinámicas en funciones:
```py
def do_something(param: _T) -> _T:
    ...
a = do_something(5) # `a` se tipa como entero
b = do_something('Onnymm') # `b` se tipa como cadena de texto
c = do_something(True) # `c` se tipa como booleano
```

Este tipo de dato también se puede usar para transformación de tipos de dato de entradas y salidas:
```py
def get_first_item(iterable_object: list[_T]) -> _T:
    return iterable_object[0]
a = get_first_item([1, 2, 3]) # `a` se tipa como entero
b = get_first_item(['uno', 'dos', 'tres']) # `b` se tipa como cadena de texto
c = get_first_item([True, False]) # `c` se tipa como booleano
```

#### `_E` Tipo de dato genérico
```py
_E = TypeVar('_E')
```

Tipo de dato usado para declarar un valor extraído de una colección de datos.

#### `_C` Tipo de dato genérico
```py
_C_ = TypeVar('_C_')
```

Tipo de dato usado para declarar un valor base para ser usado como criterio de clasificación de grupos de datos.

### Filtros

#### `ComparisonOperator` Operador de comparación
```py
ComparisonOperator = Literal[
    '=',
    '!=',
    '>',
    '>=',
    '<',
    '<=',
    '><',
    'in',
    'not in',
    'ilike',
    'not ilike',
    '~',
    '~*',
]
```
Tipo de dato que representa una operador de comparación.

Los operadores de comparación disponibles son:
- `'='`: Igual a
- `'!='`: Diferente de
- `'>'`: Mayor a
- `'>='`: Mayor o igual a
- `'<`': Menor que
- `'<='`: Menor o igual que
- `'><'`: Entre
- `'in'`: Está en
- `'not in'`: No está en
- `'ilike'`: Contiene
- `'not ilike'`: No contiene
- `'~'`: Coincide con expresión regular (sensible a mayúsculas y minúsculas)
- `'~*'`: Coincide con expresión regular (no sensible a mayúsculas y minúsculas)

#### `LogicOperator` Operador lógico
```py
LogicOperator = Literal['&', '|']
```
Tipo de dato que representa un operador lógico.

Los operadores lógicos disponibles son:
- `'&'`: AND
- `'|'`: OR

#### `TripletStructure` Estructura de tripletas para queries SQL
```py
TripletStructure = tuple[str, ComparisonOperator, RecordValue]
```
Este tipo de dato representa una condición sencilla para usarse en una transacción en base de datos.

La estructura de una tripleta consiste en 3 diferentes parámetros:
1. Nombre del campo del modelo
2. Operador de comparación
3. Valor de comparación

Algunos ejemplos de tripletas son:
```py
('name', '=', 'Onnymm')
# Nombre es igual a "Onnymm"
('id', '=', 5)
# ID es igual a 5
('amount', '>', 500)
# "amount" es mayor a 500
('name', 'ilike', 'as')
# "name" contiene "as"
```

> Para saber más sobre los tipos de datos usados consulta:
> - [`ComparisonOperator` Operador de comparación](#comparisonoperator-operador-de-comparación)

#### `CriteriaStructure` Estructura de criterio de búsqueda
```py
CriteriaStructure = list[ Union[LogicOperator, TripletStructure] ]
```

La estructura del criterio de búsqueda consiste en una lista de dos tipos de dato:
- `TripletStructure`: Estructura de tripletas para queries SQL
- `LogicOperator`: Operador lógico

Estas tuplas deben contenerse en una lista. En caso de haber más de una condición, se deben unir por operadores lógicos `'AND'` u `'OR'`. Siendo el operador lógico el que toma la primera posición:
```py
['&', ('amount', '>', 500), ('name', 'ilike', 'as')]
# "amount" es mayor a 500 y "name" contiene "as"
['|', ('id', '=', 5), ('state', '=', 'posted')]
# "id" es igual a 5 o "state" es igual a "posted"
```

> Para saber más sobre los tipos de datos usados consulta:
> - [ `LogicOperator` Operador lógico](#logicoperator-operador-lógico)
> - [`TripletStructure` Estructura de tripletas para queries SQL](#tripletstructure-estructura-de-tripletas-para-queries-sql)

### Literales

#### `ExecutionMethod` Método de validación
```py
ExecutionMethod = Literal['record', 'list']
```
Tipo de dato usado para especificar el método de ejecución que una función de automatización o validación va a utilizar.
- `'record'`: Ejecución por registro.
- `'list'`: Ejecución por lista de registros.

#### `ModelName` Nombre de modelo
```py
ModelName = Literal[
    'base.model',
    'base.model.field',
    'base.model.field.selection',
    'base.users',
]
```
Nombre de modelo base de la base de datos.

Nombres disponibles:
- `'base.model'`: Modelos
- `'base.model.field'`: Campos
- `'base.model.field.selection'`: Valores de selección
- `'base.users'`: Usuarios

#### `ModificationTransaction` Transacción de modificación
```py
ModificationTransaction = Literal['create', 'update']
```
Tipo de dato usado para especificación de transacciones de modificación en la base de datos.
- `'create'`: Método de creación en la base de datos
- `'update'`: Método de modificación en la base de datos

#### `OutputOptions` Salida de datos
```py
OutputOptions = Literal['dataframe', 'dict']
```
Opciones de salida de datos.

#### `Submodule` Nombre de submódulo de Lylac
```py
Submodule = Literal[
    '_automations',
    '_ddl',
    '_strc',
    '_validations',
]
```
Tipo de dato usado para apuntar hacia algún submódulo de la librería.

Valores disponibles:
- `'_automations'`: Módulo de automatizaciones
- `'_ddl'`: Módulo de definición de datos de la base de datos
- `'_strc'`: Módulo de la estructura de la base de datos
- `'_validations'`: Módulo de validaciones

#### `Transaction` Transación de base de datos
```py
Transaction = Union[ModificationTransaction, Literal['delete']]
```
Tipo de dato usado para especificación de transacción en la base de datos. Se omite el método `'select'` ya que no se utiliza para este tipado.
- `'create'`: Método de creación en la base de datos
- `'update'`: Método de modificación en la base de datos
- `'delete'`: Método de eliminación en la base de datos

> Para saber más sobre los tipos de datos usados consulta:
> - [`RecordValue` Valor de registro](#recordvalue-valor-de-registro)

#### `TType` Tipo de dato en campo de modelo en la base de datos
```py
TType = Literal[
    'integer',
    'char',
    'float',
    'boolean',
    'date',
    'datetime',
    'time',
    'file',
    'text',
    'selection',
    'many2one',
    'one2many',
    'many2many',
]
```
Tipo de dato válido en un campo de un modelo de la base de datos.
- `'integer'`: Entero
- `'char'`: Cadena de texto
- `'float'`: Flotante
- `'boolean'`: Booleano
- `'date'`: Fecha
- `'datetime'`: Fecha y hora
- `'time'`: Hora
- `'file'`: Archivo binario
- `'text'`: Texto largo
- `'selection'`: Selección
- `'many2one'`: Muchos a uno
- `'one2many'`: Uno a muchos
- `'many2many'`: Muchos a muchos

### Modelos

#### `DataBaseDataType` Tipo de dato de SQLAlchemy
```py
DataBaseDataType = Union[
    type[Integer],
    type[String],
    type[Float],
    type[Boolean],
    type[Date],
    type[DateTime],
    type[Time],
    type[Text],
    type[LargeBinary],
]
```
Tipo de dato de atributos de modelos de SQLAlchemy.

----

## Tipados de diccionarios

### Diccionarios de datos

#### `AutomationData` Datos de registro de automatización
```py
class AutomationData(TypedDict):
    # Nombre de submódulo de Lylac
    submodule: Submodule
    # Función
    callback: str
    # Nombre de modelo
    model: ModelName
    # Transación de base de datos
    transaction: Transaction
    # Estructura de criterio de búsqueda
    criteria: CriteriaStructure
    # Lista de campos
    fields: list[str]
    # Método de automatización
    method: AutomationMethod
```
Estructura de diccionario de datos.

Uso:
```py
data = {
    # Nombre de submódulo de Lylac
    'submodule': '_automations',
    # Función
    'callback': 'some_automation',
    # Nombre de modelo
    'model': 'base.model',
    # Transación de base de datos
    'transaction': 'create',
    # Estructura de criterio de búsqueda
    'criteria': [('state', '!=', 'base')],
    # Lista de campos
    'fields': ['name', 'model'],
    # Método de automatización
    'method': 'record',
}
```

> Para saber más sobre los tipos de datos usados consulta:
> - [`Submodule` Nombre de submódulo de Lylac](#submodule-nombre-de-submódulo-de-lylac)
> - [`ModelName` Nombre de modelo](#modelname-nombre-de-modelo)
> - [`Transaction` Transación de base de datos](#transaction-transación-de-base-de-datos)
> - [`CriteriaStructure` Estructura de criterio de búsqueda](#criteriastructure-estructura-de-criterio-de-búsqueda)
> - [`AutomationMethod` Método de automatización](#automationmethod-método-de-automatización)

#### `ValidationData` Datos de registro de validación
```py
class ValidationData(TypedDict):
    # Nombre de submódulo de Lylac
    submodule: Submodule
    # Función
    callback: str
    # Transación de base de datos
    transaction: Transaction
    # Método de ejecución
    method: ExecutionMethod
    # Mensaje de error
    message: str
```
Estructura de diccionario de datos.

Uso:
```py
{
    # Nombre de submódulo de Lylac
    'submodule': '_validations',
    # Función
    'callback': 'some_validation',
    # Nombre de modelo
    'model': 'base.model',
    # Transación de base de datos
    'transaction': 'create',
    # Método de validación
    'method': 'record',
    # Mensaje de error
    'message': 'El valor {value} no cumple con el formato esperado.'
}
```

> Para saber más sobre los tipos de datos usados consulta:
> - [`Submodule` Nombre de submódulo de Lylac](#submodule-nombre-de-submódulo-de-lylac)
> - [`ModelName` Nombre de modelo](#modelname-nombre-de-modelo)
> - [`Transaction` Transación de base de datos](#transaction-transación-de-base-de-datos)
> - [`ExecutionMethod` Método de validación](#executionmethod-método-de-validación)

### Diccionarios de credenciales

#### `CredentialsArgs` Credenciales de la base de datos
```py
class CredentialsArgs(TypedDict):
    # Dirección URL en donde se aloja la base de datos.
    host: str
    # Puerto del host en donde se aloja la base de datos.
    port: int
    # Nombre de la base de datos.
    db_name: str
    # Nombre de usuario de acceso a la base de datos.
    user: str
    # Contraseña de acceso a la base de datos.
    password: str
```
Diccionario contenedor de los valores de credenciales para conexión con la base de datos.

Uso:
```py
{
    'host': 'https://www.db_host.com',
    'port': 5432,
    'db_name': 'my_database',
    'user': 'postgresql',
    'password': 'somepassword123'
}
```

### Diccionarios de estructura de base de datos

#### `FieldProperties` Propiedades de campo

```py
class FieldProperties(TypedDict):
    # Tipo de dato en campo de modelo en la base de datos
    ttype: TType
    # Modelo relacionado
    related_model: ModelName
    # Campo relacionado
    related_field: str
```
Diccionario que almacena el tipo de dato y la relación de un campo.

Uso:
```py
{
    'ttype': 'many2one',
    'relation': 'base.users',
}
```

> Para saber más sobre los tipos de datos usados consulta:
> - [`TType` Tipo de dato en campo de modelo en la base de datos](#ttype-tipo-de-dato-en-campo-de-modelo-en-la-base-de-datos)
> - [`ModelName` Nombre de modelo](#modelname-nombre-de-modelo)

#### `ModelMap` Mapa de atributos de modelo
```py
class ModelMap(TypedDict):
    # Modelo SQLAlchemy de la tabla
    model: type[DeclarativeBase]
    # Diccionario que almacena el tipo de dato y la relación de un campo.
    fields: dict[str, FieldProperties]
```
Este tipo de dato almacena la información básica que define la estructura de un modelo almacenado en una instancia Lylac.

Uso:
```py
{
    'model': <ModelInstance>,
    'fields': {
        'id': {
            'ttype': 'integer',
            'related_model': None,
            'related_field': None,
        },
        'write_uid': {
            'ttype': 'many2one',
            'related_model': 'base.users',
            'related_field': None,
        },
        'category_ids': {
            'ttype': 'one2many',
            'related_model': 'product.category',
            'related_field': 'product_id',
        },
        ...
    },
}
```

> Para saber más sobre los tipos de datos usados consulta:
> - [`FieldProperties` Propiedades de campo](#fieldproperties-propiedades-de-campo)

### Diccionarios de registros

#### `NewRecord` Nuevo registro
```py
class NewRecord():
    class Model(TypedDict):
        ...
    class ModelField(TypedDict):
        ...
    class ModelFieldSelection(TypedDict):
        ...
    class User(TypedDict):
        ...
```
Estructuras de diccionarios para la creación de nuevos registros en los modelos predeterminados de Lylac.

Los subtipos disponibles son:
- `Model`: Nuevo registro de modelo
- `ModelField`: Nuevo registro de campo
- `ModelFieldSelection`: Nuevo registro de selección de campo
- `User`: Nuevo registro de usuario

> #### `Model` Nuevo registro de modelo
> ```py
> class Model(TypedDict):
>     # Nombre
>     name: str
>     # Etiqueta
>     label: str
>     # Nombre de modelo
>     model: ModelName
>     # Descripción
>     description: str
> ```
> Uso:
> ```py
> {
>     # Nombre
>     'name': 'my_model',
>     # Nombre de modelo
>     'model': 'my.model',
>     # Etiqueta
>     'label': 'Mi modelo',
>     # Descripción
>     'description': 'Modelo personalizado en la base de datos.'
> }
> ```
>> Para saber más sobre los tipos de datos usados consulta:
>> - [`ModelName` Nombre de modelo](#modelname-nombre-de-modelo)
> 
> #### `ModelField` Nuevo registro de campo
> ```py
> class ModelField(TypedDict):
>     # Nombre
>     name: str
>     # Etiqueta
>     label: str
>     # Tipo de dato en campo de modelo en la base de datos
>     ttype: TType
>     # ID de modelo
>     model_id: int
>     # Puede ser nulo
>     nullable: bool
>     # Es único
>     unique: bool
>     # Requerido
>     is_required: bool
>     # Valor predeterminado
>     default_value: Optional[str]
>     # Información
>     help_info: str | None
>     # ID de modelo relacionado
>     related_model_id: int | None
> ```
> Uso:
> ```py
> {
>     # Nombre
>     'name': 'my_field',
>     # Etiqueta
>     'label': 'Mi campo',
>     # Tipo de dato en campo de modelo en la base de datos
>     'ttype': 'char',
>     # ID de modelo
>     'model_id': 5,
>     # Valor predeterminado
>     'default_value': 'Mi valor predeterminado',
>     # Puede ser nulo
>     'nullable': True,
>     # Es único
>     'unique': False,
> }
> ```
>> Para saber más sobre los tipos de datos usados consulta:
>> - [`TType` Tipo de dato en campo de modelo en la base de datos](#ttype-tipo-de-dato-en-campo-de-modelo-en-la-base-de-datos)
> 
> #### `ModelFieldSelection` Nuevo registro de selección de campo
> ```py
> class ModelFieldSelection(TypedDict):
>     # Nombre
>     name: str
>     # Etiqueta
>     label: str
>     # ID de campo
>     field_id: int
> ```
> Uso:
> ```py
> {
>     # Nombre
>     'name': 'value_1',
>     # Etiqueta
>     'label': 'Valor 1',
>     # ID de campo
>     'field_id': 25,
> }
> ```
> 
> #### `User` Nuevo registro de usuario
> ```py
> class User(TypedDict):
>     # Nombre
>     name: str
>     # Nombre de usuario
>     login: str
>     # ID de Odoo
>     odoo_id: int
>     # Sincronizar
>     sync: bool
> ```
> Uso:
> ```py
> {
>     # Nombre
>     'name': 'Onnymm',
>     # Nombre de usuario
>     'login': 'onnymm',
>     # ID de Odoo
>     'odoo_id': 5,
>     # Sincronizar
>     'sync': False,
> }
> ```

#### `ModelRecordData` Datos de registros en la base de datos
```py
class ModelRecordData:
    class BaseModel_(TypedDict...):
        ...
    class BaseModelField(TypedDict...):
        ...
    class BaseModelFieldSelection(TypedDict...):
        ...
    class BaseUsers(TypedDict...):
        ...
```
Tipados de datos de registros de diferentes modelos en la base de datos.
- `BaseModel_`: Datos de modelos
- `BaseModelField`: Datos de campos
- `BaseModelFieldSelection`: Datos de valores de selección de campos
- `BaseUsers`: Datos de usuarios

> #### `BaseModel_` Datos de modelo
> ```py
> {
>     # ID del registro
>     'id': 1,
>     # Nombre del registro
>     'name': 'base_model',
>     # Fecha de creación
>     'create_date': '2025-07-01-10:00:00',
>     # Fecha de modificación
>     'write_date': '2025-07-01-10:00:00',
>     # Usuario de creación
>     'create_uid': 1,
>     # Usuario de modificación
>     'write_uid': 1,
>     # Etiqueta
>     'label': 'Modelos',
>     # Tipo
>     'state': 'base',
>     # Nombre del modelo
>     'model': 'base.model',
>     # Descripción
>     'description': '...',
>     # Campos
>     'field_ids': [1, 2, 3, ...],
>     # Campos relacionados al modelo
>     'related_field_ids': [5, 8, ...],
> }
> ```
> 
> #### `BaseModelField` Datos de campo
> ```py
> {
>     # ID del registro
>     'id': 1,
>     # Nombre del registro
>     'name': 'nullable',
>     # Fecha de creación
>     'create_date': '2025-07-01-10:00:00',
>     # Fecha de modificación
>     'write_date': '2025-07-01-10:00:00',
>     # Usuario de creación
>     'create_uid': 1,
>     # Usuario de modificación
>     'write_uid': 1,
>     # Etiqueta
>     'label': 'Puede ser nulo',
>     # Tipo
>     'state': 'base',
>     # ID de modelo
>     'model_id': 2,
>     # Tipo de dato en campo
>     'ttype': 'boolean',
>     # Puede ser nulo
>     'nullable': True,
>     # Es requerido
>     'is_required': False,
>     # Valor predeterminado
>     'default_value': None,
>     # Es valor único
>     'unique': False,
>     # Información de ayuda
>     'help_info': '...',
>     # Modelo relacionado
>     'related_model_id': None,
>     # Campo relacionado
>     'related_field': None,
>     # Valores de selección
>     'selection_ids': [],
> }
> ```
> 
> #### `BaseModelFieldSelection` Datos de valores de selección de campo
> ```py
> {
>     # ID del registro
>     'id': 2,
>     # Nombre del registro
>     'name': 'generic',
>     # Fecha de creación
>     'create_date': '2025-07-01-10:00:00',
>     # Fecha de modificación
>     'write_date': '2025-07-01-10:00:00',
>     # Usuario de creación
>     'create_uid': 1,
>     # Usuario de modificación
>     'write_uid': 1,
>     # Etiqueta
>     'label': 'Puede ser nulo',
>     # ID de campo
>     'field_id': 8,
> }
> ```
> 
> #### `BaseUsers` Datos de usuario
> ```py
> {
>     # ID del registro
>     'id': 1,
>     # Nombre del registro
>     'name': 'iaCele',
>     # Fecha de creación
>     'create_date': '2025-07-01-10:00:00',
>     # Fecha de modificación
>     'write_date': '2025-07-01-10:00:00',
>     # Usuario de creación
>     'create_uid': 1,
>     # Usuario de modificación
>     'write_uid': 1,
>     # Está activo
>     'active': True,
>     # Sincronizar
>     'sync': False,
>     # Nombre de usuario
>     'login': 'iacele',
>     # ID de Odoo
>     'odoo_id': None,
>     # Contraseña
>     'password': '...',
> }
> ```

----

## Tipados de modelos

### Modelos de automatizaciones

#### `AutomationModel` Automatización
```py
class AutomationModel(BaseModel):
    # Nombre de submódulo de Lylac
    submodule: Submodule
    # Función
    callback: str
    # Nombre de modelo
    model: ModelName
    # Transación de base de datos
    transaction: Transaction
    # Estructura de criterio de búsqueda
    criteria: CriteriaStructure
    # Lista de campos
    fields: list[str]
    # Método de automatización
    method: AutomationMethod
```
Modelo de datos de automatización

> Para saber más sobre los tipos de datos usados consulta:
> - [`AutomationMethod` Método de automatización](#automationmethod-método-de-automatización)
> - [`CriteriaStructure` Estructura de criterio de búsqueda](#criteriastructure-estructura-de-criterio-de-búsqueda)
> - [`ModelName` Nombre de modelo](#modelname-nombre-de-modelo)
> - [`Submodule` Nombre de submódulo de Lylac](#submodule-nombre-de-submódulo-de-lylac)
> - [`Transaction` Transación de base de datos](#transaction-transación-de-base-de-datos)

#### `DataPerRecord` Datos por registro
```py
class DataPerRecord(BaseModel, _T):
    #### ID
    id: int
    #### Datos del registro
    record_data: _T
```
Tipado usado para argumento de entrada de funciones que se usan como automatizaciones. Este tipo de dato está incompleto y requiere tener especificado un tipo de registro. De esta manera se puede mejorar la programación de la automatización.

Uso:
```py
def my_automation(
    params: DataPerTransaction[ModelRecord.BaseModel_],
) -> None:
    # Se procesan los registros
    ...
```
> Para saber más sobre los tipos de datos usados consulta:
> - [`_T` Tipo de dato genérico](#_t-tipo-de-dato-genérico)
> - [`NewRecord` Nuevo registro](#newrecord-nuevo-registro)

#### `DataPerTransaction` Datos por transacción
```py
class DataPerTransaction(BaseModel, Generic[_T]):
    # IDs
    ids: list[int]
    # Datos de los registros
    records_data: list[_T]
```
Tipado usado para argumento de entrada de funciones que se usan como automatizaciones. Este tipo de dato está incompleto y requiere tener especificado un tipo de registro. De esta manera se puede mejorar la programación de la automatización.

Uso:
```py
def my_automation(
    params: DataPerTransaction[ModelRecord.BaseModel_],
) -> None:
    # Se procesan los registros
    ...
```
> Para saber más sobre los tipos de datos usados consulta:
> - [`_T` Tipo de dato genérico](#_t-tipo-de-dato-genérico)
> - [`NewRecord` Nuevo registro](#newrecord-nuevo-registro)

### Modelos de definiciones

#### `FieldDefinition` Definición de campo
```py
class FieldDefinition(BaseModel):
    #  Nombre del campo.
    field_name: str
    #  Modelo de la tabla.
    table_model: type[DeclarativeBase]
    #  Etiqueta de la tabla.
    label: str
    #  Tipo de dato del campo.
    ttype: TType
    #  Puede ser nulo.
    nullable: bool =  False
    #  Es requerido.
    is_required: bool = False
    #  Valor predeterminado.
    default: Optional[RecordValue] = None
    #  Único.
    unique: bool = False
    #  Información de ayuda del campo.
    help_info: Optional[str] = None
    #  ID de modelo relacionado.
    related_model_id: Optional[int] = None
```
Modelo base para crear objetos de campo nuevo para usarse en automatizaciones de creación de modelos de SQLAlchemy, tablas de base de datos y sus respectivos campos.
> Para saber más sobre los tipos de datos usados consulta:
> - [`RecordValue` Valor de registro](#recordvalue-valor-de-registro)
> - [`TType` Tipo de dato en campo de modelo en la base de datos](#ttype-tipo-de-dato-en-campo-de-modelo-en-la-base-de-datos)

### Modelos de credenciales

#### `CredentialsFromEnv` Credenciales de la base de datos
Objeto contenedor de los valores de credenciales para conexión con la base de datos.
```py
class Credentials(BaseModel):
    # Dirección URL en donde se aloja la base de datos.
    host: str
    # Puerto del host en donde se aloja la base de datos.
    port: str
    # Nombre de la base de datos.
    db_name: str
    # Nombre de usuario de acceso a la base de datos.
    user: str
    # Contraseña de acceso a la base de datos.
    password: str
```


## Tipados de funciones

### Funciones internas

#### `AutomationTemplate` Función de automatización
```py
AutomationTemplate = Callable[[DataPerRecord | DataPerTransaction], None]
```
Estructura que debe tener una función para registrarse como automatización.
> Para saber más sobre los tipos de datos usados consulta:
> - [`DataPerRecord` Datos por registro](#dataperrecord-datos-por-registro)
> - [`DataPerTransaction` Datos por transacción](#datapertransaction-datos-por-transacción)

----

## Tipados complejos

### Argumentos de funciones

#### `CredentialsAlike` Credenciales de acceso a la base de datos
```py
CredentialsAlike = Union[CredentialsArgs, str, None]
```
Diccionario contenedor de los valores de credenciales para conectar o URL de conexión con la base de datos.

Uso:
```py
# Formato de diccionario
{
    'host': 'https://www.db_host.com',
    'port': 5432,
    'db_name': 'my_database',
    'user': 'postgresql',
    'password': 'somepassword123'
}
# Formato de URL
f"postgresql+psycopg2://postgres:{password}@{host}:{port}/{database_name}"
```

### Retornos de funciones

#### `DataOutput` Tipo de dato retornado
```py
DataOutput = Union[pd.DataFrame | dict[str, RecordValue]]
```
Tipo de dato retornado por métodos de lectura en el módulo principal.
