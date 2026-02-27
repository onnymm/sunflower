from typing import Any
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.attributes import InstrumentedAttribute
from ..._module_types import ModelName

class Models_Interface():

    def get_model_name(
        self,
        model_model: type[DeclarativeBase],
    ) -> ModelName:
        ...

    def get_model_model(
        self,
        model_name: ModelName,
    ) -> type[DeclarativeBase]:
        ...

    def get_id_field(
        self,
        model_model: type[DeclarativeBase]
    ) -> InstrumentedAttribute[int]:
        ...

    def get_model_field(
        self,
        model_model: type[DeclarativeBase],
        field: str,
    ) -> InstrumentedAttribute:
        ...

    def get_model_fields(
        self,
        model_model: type[DeclarativeBase],
        fields: list[str] = [],
        include_id: bool = True,
    ) -> list[InstrumentedAttribute[Any]]:
        ...
