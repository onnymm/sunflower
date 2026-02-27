from sqlalchemy.orm.decl_api import DeclarativeBase
from ...._module_types import (
    FieldDefinition,
    ModelRecordData,
    ModelName,
)

class _Models_Interface():

    def create_model(
        self,
        model_name: ModelName,
    ) -> type[DeclarativeBase]:
        ...

    def create_relation(
        self,
        owner_model_name: ModelName,
        referenced_model_name: ModelName,
    ) -> type[DeclarativeBase]:
        ...

    def delete_model(
        self,
        model_name: ModelName,
    ) -> None:
        ...

    def add_field_to_model(
        self,
        model_model: type[DeclarativeBase],
        field: FieldDefinition,
    ) -> None:
        ...

    def build_field_atts(
        self,
        params: ModelRecordData.BaseModelField,
    ) -> FieldDefinition:
        ...
