from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm.decl_api import DeclarativeBase
from .._base import RecordValue
from .._base_categories import TTypeName

class FieldDefinition(BaseModel):
    """
    ### Definición de campo
    Modelo base para crear objetos de campo nuevo para usarse en automatizaciones
    de creación de modelos de SQLAlchemy, tablas de base de datos y sus respectivos
    campos.
    >>> class FieldDefinition(BaseModel):
    >>>     # Nombre del campo
    >>>     field_name: str
    >>>     # Modelo de la tabla
    >>>     table_model: type[DeclarativeBase]
    >>>     # Etiqueta de la tabla
    >>>     label: str
    >>>     # Tipo de dato del campo
    >>>     ttype: TType
    >>>     # Puede ser nulo
    >>>     nullable: bool =  False
    >>>     # Es requerido
    >>>     is_required: bool = False
    >>>     # Valor predeterminado
    >>>     default: Optional[RecordValue] = None
    >>>     # Único
    >>>     unique: bool = False
    >>>     # Información de ayuda del campo
    >>>     help_info: Optional[str] = None
    >>>     # ID de modelo relacionado
    >>>     related_model_id: Optional[int] = None
    """
    field_name: str
    """
    Nombre del campo.
    """
    table_model: type[DeclarativeBase]
    """
    Modelo de la tabla.
    """
    label: str
    """
    Etiqueta de la tabla.
    """
    ttype: TTypeName
    """
    Tipo de dato del campo.
    """
    nullable: bool =  False
    """
    Puede ser nulo.
    """
    is_required: bool = False
    """
    Es requerido.
    """
    default: Optional[RecordValue] = None
    """
    Valor predeterminado.
    """
    unique: bool = False
    """
    Único.
    """
    help_info: Optional[str] = None
    """
    Información de ayuda del campo.
    """
    related_model_id: Optional[int] = None
    """
    ID de modelo relacionado.
    """
    is_computed: bool = False
    """
    Es un campo computado.
    """
