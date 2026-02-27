from typing import (
    Literal,
    Union,
)

SubmoduleName = Literal[
    '_actions',
    '_automations',
    '_ddl',
    '_strc',
    '_validations',
    '_compute',
]
"""
#### Nombre de submódulo de Lylac
Tipo de dato usado para apuntar hacia algún submódulo de la librería.

Valores disponibles:
- `'_automations'`: Módulo de automatizaciones
- `'_ddl'`: Módulo de definición de datos de la base de datos
- `'_strc'`: Módulo de la estructura de la base de datos
- `'_validations'`: Módulo de validaciones
"""

# Nombre de tipo dato en columnas base de datos
TTypeName = Literal[
    'integer',
    'char',
    'float',
    'boolean',
    'date',
    'datetime',
    'time',
    'duration',
    'file',
    'text',
    'selection',
    'many2one',
    'one2many',
    'many2many',
]
"""
#### Tipo de dato en campo de modelo en la base de datos
Tipo de dato válido en un campo de un modelo de la base de datos.
- `'integer'`: Entero
- `'char'`: Cadena de texto
- `'float'`: Flotante
- `'boolean'`: Booleano
- `'date'`: Fecha
- `'datetime'`: Fecha y hora
- `'time'`: Hora
- `'duration'`: Duración en tiempo
- `'file'`: Archivo binario
- `'text'`: Texto largo
- `'selection'`: Selección
- `'many2one'`: Muchos a uno
- `'one2many'`: Uno a muchos
- `'many2many'`: Muchos a muchos
"""

State = Literal['base', 'generic']
"""
#### Tipo de registro
Valor que indica si el registro es parte de los datos iniciales de la base de
datos (`'base'`) o es parte de los datos creados posteriormente (`'generic'`).
"""

# Método de ejecución
ExecutionMethod = Literal['record', 'list']
"""
#### Método de ejecución
Tipo de dato usuado para especificar el método de ejecución de una
automatización o validación.
- `'record'`: Validación por registro.
- `'list'`: Validación por lista de registros.
"""

# Método de ejecución de automatización
AutomationMethodName = Literal['record', 'list']
"""
#### Método de automatización
Tipo de dato usado para especificar el método de automatización que una
función de automatización va a utilizar.
- `'record'`: Automatización por registro.
- `'list'`: Automatización por lista de registros.
"""

# Tipo de transacción de creación o actualización de datos
UpsertTransactionName = Literal['create', 'update']
"""
#### Transacción de creación o actualización en base de datos
Tipo de dato usado para especificación de transacciones de creación o
modificación en la base de datos.
- `'create'`: Método de creación en la base de datos
- `'update'`: Método de modificación en la base de datos
"""

# Tipo de transacción de modificación de datos
WriteTransactionName = Union[UpsertTransactionName, Literal['delete']]
"""
#### Transación de modificación en base de datos
Tipo de dato usado para especificación de transacción de modificación en la
base de datos.
- `'create'`: Método de creación en la base de datos
- `'update'`: Método de modificación en la base de datos
- `'delete'`: Método de eliminación en la base de datos
"""

# Tipo de transacción de datos
TransactionName = Union[WriteTransactionName | Literal['read']]
"""
#### Transación en base de datos
Tipo de dato usado para especificación de transacción en la base de datos.
- `'create'`: Método de creación en la base de datos
- `'read'`: Método de lectura en la base de datos
- `'update'`: Método de modificación en la base de datos
- `'delete'`: Método de eliminación en la base de datos
"""

# Modelos base de la base de datos
ModelName = Literal[
    'base.model',
    'base.model.field',
    'base.model.field.selection',
    'base.users',
    'base.model.access',
    'base.model.access.groups',
    'base.users.role',
    'base.users.session',
]
"""
#### Nombre de modelo
Nombre de modelo base de la base de datos.

Nombres disponibles:
- `'base.model'`: Modelos
- `'base.model.field'`: Campos
- `'base.model.field.selection'`: Valores de selección
- `'base.users'`: Usuarios
"""

# Opciones de salida de datos
OutputOptions = Literal['dataframe', 'dict']
"""
### Salida de datos
Opciones de salida de datos.
>>> Literal['dataframe', 'dict']
"""

AggFunctionName = Literal['sum', 'count']
"""
#### Nombre de función de agregación
Nombre de función de agregación para usarse en indexación de funciones de agregación.
Nombres disponibles
- `'sum'`: Función de suma.
- `'count'`: Función de conteo.
"""

SubtransactionName = Literal['create', 'update', 'delete', 'unlink', 'add', 'clean', 'replace']
"""
### Nombre de subtransacción
Nombre de subtransacción de valores many2many.

Los valores disponibles son:
- `'create'`: Creación de registros
- `'update'`: Actualización de registros
- `'delete'`: Eliminación de registros
- `'add'`: Vinculación de registros
- `'unlink'`: Desvinculación de registros
- `'clean'`: Limpieza de registros
- `'replace'`: Reemplazo de registros
"""

SubtransactionCreateMode = Literal['create']
"""
Modo de subtransacción en creación.
"""

SubtransactionUpdateMode = Literal['update']
"""
Modo de subtransacción en actualización.
"""

SubtransactionMode = Union[SubtransactionCreateMode, SubtransactionUpdateMode]
"""
### Modo de subtransacción
Los valores disponibles son:
- `'create'`: Creación
- `'update'`: Actualización
"""

ToCast = Literal['integer', 'char', 'boolean', 'date', 'datetime', 'time', 'duration']
"""
### Tipos de dato disponibles para casteo
Tipos de dato que pueden usarse para convertir el tipo de dato de un campo en
otro que se desee usar.
"""
