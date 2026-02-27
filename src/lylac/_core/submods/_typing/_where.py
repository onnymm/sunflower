from typing import Callable
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.elements import BinaryExpression
from ...._module_types import RecordValue

# Función de comparación
ComparisonCallback = Callable[[InstrumentedAttribute, RecordValue], BinaryExpression]
"""
### Función de comparación
Función que realiza la creación de fragmentos de query SQL que indican la
comparación de una columna de una tabla de la base de datos con un valor o una
colección de valores.
>>> def equals_to(field: InstrumentedAttribute, value: TripletValue) -> BinaryExpression
>>>     return field == TripletValue
>>> 
>>> def contains(field: InstrumentedAttribute, value: TripletValue) -> BinaryExpression
>>>     return field.contains(value)
"""

# Función de conjunción/disyunción
ConditionUnionCallback = Callable[[BinaryExpression, BinaryExpression], BinaryExpression]
"""
### Función de unión de queries
Función para unir dos queries ya sea por un `OR` o un `AND`
>>> def or_(condition_1: BinaryExpression, condition_2: BinaryExpression) -> BinaryExpression
>>>     return sqlalchemy.or_(condition_1, condition_2)
"""
