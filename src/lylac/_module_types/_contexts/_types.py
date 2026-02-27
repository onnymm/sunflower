from typing import (
    Callable,
    Union,
)
from sqlalchemy.orm import InstrumentedAttribute
from ._interfaces import _ComputeContextCore
from .._base_categories import TTypeName
from .._interface import ModelField

ComputedFieldCallback = Callable[[_ComputeContextCore], InstrumentedAttribute]
"""
#### Función de cómputo de campo
Función lambda usada para declarar el cómputo de un campo

Uso:
>>> # Obtención de un subtotal de línea de venta
>>> lambda ctx: ctx['price'] * ctx['quantity']
>>> 
>>> # Obtención de un conteo
>>> lambda ctx: ctx.agg('fields', 'count')
>>> 
>>> # Obtención de un subtotal de venta
>>> lambda ctx: ctx.agg('lines.subtotal', 'sum')
>>> 
>>> # Valores condicionales
>>> lambda ctx: ctx.case(
>>>     (ctx['quantity'] > 5, True),
>>>     default= False
>>> )
"""

FieldComputation = tuple[str, TTypeName, ComputedFieldCallback]
"""
#### Declaración de un campo computado
Estructura para ser utilizada en la creación y tipado de un campo computado.

Ejemplo:
>>> ('subtotal', 'float', lambda ctx: ctx['price'] * ctx['quantity'])

#### Función de cómputo de campo
Función lambda usada para declarar el cómputo de un campo

Uso:
>>> # Obtención de un subtotal de línea de venta
>>> lambda ctx: ctx['price'] * ctx['quantity']
>>> 
>>> # Obtención de un conteo
>>> lambda ctx: ctx.agg('fields', 'count')
>>> 
>>> # Obtención de un subtotal de venta
>>> lambda ctx: ctx.agg('lines.subtotal', 'sum')
>>> 
>>> # Valores condicionales
>>> lambda ctx: ctx.case(
>>>     (ctx['quantity'] > 5, True),
>>>     default= False
>>> )
"""

DynamicModelField = Union[ModelField, FieldComputation]
"""
#### Campo dinámico de modelo
Unión de declaraciones de campos, alias de campos y campos computados

Ejemplo:
>>> fields = [
>>>     # Campos reales en la tabla
>>>     'name',
>>>     'create_date',
>>>     # Alias de 'label' a 'description'
>>>     ('label', 'description'),
>>>     # Campo computado
>>>     ('subtotal', 'float', lambda ctx: ctx['price'] * ctx['quantity']),
>>> ]

#### Declaración de un campo computado
Estructura para ser utilizada en la creación y tipado de un campo computado.

Ejemplo:
>>> ('subtotal', 'float', lambda ctx: ctx['price'] * ctx['quantity'])

#### Función de cómputo de campo
Función lambda usada para declarar el cómputo de un campo

Uso:
>>> # Obtención de un subtotal de línea de venta
>>> lambda ctx: ctx['price'] * ctx['quantity']
>>> 
>>> # Obtención de un conteo
>>> lambda ctx: ctx.agg('fields', 'count')
>>> 
>>> # Obtención de un subtotal de venta
>>> lambda ctx: ctx.agg('lines.subtotal', 'sum')
>>> 
>>> # Valores condicionales
>>> lambda ctx: ctx.case(
>>>     (ctx['quantity'] > 5, True),
>>>     default= False
>>> )
"""
