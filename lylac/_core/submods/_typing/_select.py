from typing import Any
from sqlalchemy.orm.decl_api import DeclarativeBase
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.elements import BinaryExpression
from ...._module_types import TTypesMapping

class OperationData():

    def __init__(
        self,
    ) -> None:

        # Lista de instancias de campo
        self.field_instances: list[InstrumentedAttribute[Any]] = []
        # Lista de nombres de campo con su tipo de dato
        self.ttypes_mapping: TTypesMapping = []
        # Lista de parámetros para creación de JOINs
        self.outerjoins: list[tuple[type[DeclarativeBase], BinaryExpression]] = []
