from ..._module_types import (
    ModelRecordData,
    NewRecord,
    ModelName,
)

class DDL_Interface():

    def new_table(
        self,
        model_name: ModelName,
    ) -> None:
        ...

    def new_relation(
        self,
        owner_model_name: ModelName,
        referenced_model_name: ModelName,
    ) -> None:
        ...

    def delete_relation(
        self,
        model_name: ModelName,
        field_name: str,
    ) -> None:
        ...

    def new_field(
        self,
        model_name: ModelName,
        params: ModelRecordData.BaseModelField,
    ) -> None:
        ...

    def delete_table(
        self,
        model_name: ModelName,
    ) -> None:
        ...

    def delete_field(
        self,
        model_name: ModelName,
        field_name: str,
    ) -> None:
        ...

    def add_default_to_model(
        self,
        model_id: int,
        field_names: list[str] = [],
    ) -> None:
        ...

    def build_default_field(
        self,
        field_name: str,
        model_id: int,
    ) -> NewRecord.ModelField:
        ...
