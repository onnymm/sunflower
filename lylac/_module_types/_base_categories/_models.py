from typing import Union
from sqlalchemy.types import (
    Boolean,
    Date,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    Time,
    LargeBinary,
)

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
"""
#### Tipo de dato de SQLAlchemy
Tipo de dato de atributos de modelos de SQLAlchemy.
"""
