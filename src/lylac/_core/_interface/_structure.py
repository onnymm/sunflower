from typing import Optional
from sqlalchemy.orm.decl_api import DeclarativeBase
from ..._module_types import (
    TTypeName,
    ModelName,
)

class Structure_Interface():

    def register_table(
        self,
        model_model: type[DeclarativeBase]
    ) -> None:
        ...

    def unregister_table(
        self,
        model_name: ModelName,
    ) -> None:
        ...

    def register_field(
        self,
        model_name: ModelName,
        field_name: str,
        ttype: TTypeName,
        related_model: Optional[str],
        related_field: Optional[str],
        selection_values: list[str] = [],
        is_computed: bool = False
    ) -> None:
        ...

    def unregister_field(
        self,
        model_name: ModelName,
        field_name: str,
    ) -> None:
        ...

    def register_relation(
        self,
        model_model: type[DeclarativeBase],
    ) -> None:
        ...

    def update_selection_values(
        self,
        model_name: ModelName,
        field_name: str,
        selection_values: list[str],
    ) -> None:
        ...

    def get_model(
        self,
        model_name: ModelName,
    ) -> type[DeclarativeBase]:
        ...

    def get_relation_model(
        self,
        model_name: ModelName,
        field_name: str,
    ) -> type[DeclarativeBase]:
        ...

    def get_model_names(
        self,
    ) -> list[str]:
        ...

    def get_model_field_names(
        self,
        model_name: ModelName,
    ) -> list[str]:
        ...

    def get_related_model_name(
        self,
        model_name: ModelName,
        field_name: str,
    ) -> str:
        ...

    def get_related_field_name(
        self,
        model_name: ModelName,
        field_name: str,
    ) -> str:
        ...

    def get_relation_model_name(
        self,
        model_name: ModelName,
        field_name: str,
    ) -> str:
        ...

    def get_field_ttype(
        self,
        model_name: ModelName,
        field_name: str,
    ) -> TTypeName:
        ...

    def is_computed_field(
        self,
        model_name: ModelName,
        field_name: str,
    ) -> bool:
        ...

    def get_table_name(
        self,
        model_model: type[DeclarativeBase] | str,
    ) -> str:
        ...

    def get_ttype_fields(
        self,
        model_name: ModelName,
        ttype: TTypeName,
    ) -> list[str]:
        ...

    def get_field_selection_values(
        self,
        model_name: ModelName,
        field_name: str,
    ) -> list[str]:
        ...

    def initialize_fields_atts(
        self,
    ) -> None:
        ...
