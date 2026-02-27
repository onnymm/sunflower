from typing import Any
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.decl_api import DeclarativeBase
from sqlalchemy.sql.elements import BinaryExpression
from .._module_types import (
    _SelectContextCore,
    TTypesMapping,
    TTypeName,
)

class SelectContext(_SelectContextCore):

    def __init__(
        self,
    ) -> None:

        # Lista de instancias de campo
        self.field_instances: list[InstrumentedAttribute[Any]] = []
        # Lista de nombres de campo con su tipo de dato
        self.ttypes_mapping: TTypesMapping = []
        # Lista de parámetros para creación de JOINs
        self.outerjoins: list[tuple[type[DeclarativeBase], BinaryExpression]] = []

    def add_field_instance(
        self,
        field_instance: InstrumentedAttribute[Any],
    ) -> None:

        # Se añade la instancia del campo
        self.field_instances.append(field_instance)

    def add_ttype_mapping(
        self,
        field_name: str,
        ttype: TTypeName,
    ) -> None:

        # Se añaden el nombre y el tipo del campo
        self.ttypes_mapping.append( (field_name, ttype) )

    def add_outerjoin(
        self,
        model_model: type[DeclarativeBase],
        binary_expression: BinaryExpression,
    ) -> None:

        # Se añaden el modelo y la expresión binaria
        self.outerjoins.append( (model_model, binary_expression) )
