from typing import (
    Literal,
    Union,
)
from .._base import RecordValue

# Operadores de comparación para queries SQL
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
"""
#### Operador de comparación
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
"""

# Operadores lógicos para queries SQL
LogicOperator = Literal['&', '|']
"""
#### Operador lógico
Tipo de dato que representa un operador lógico.

Los operadores lógicos disponibles son:
- `'&'`: AND
- `'|'`: OR
"""

# Estructura de tripletas para queries SQL
TripletStructure = tuple[str, ComparisonOperator, RecordValue]
"""
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

----
#### Operador de comparación
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
"""

# Estructura de criterios de búsqueda para queries SQL
CriteriaStructure = list[ Union[LogicOperator, TripletStructure] ]
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

RecordIDs = int | list[int]
"""
### IDs de registros
Valor entero o lista de enteros que representan IDs de registros.

>>> # Valor individual
>>> 5
>>> 
>>> # Lista de valores
>>> [5, 6, 7]
"""
