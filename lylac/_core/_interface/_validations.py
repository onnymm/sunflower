from ..._module_types import (
    CriteriaStructure,
    RecordData,
    ModelName,
)

class Validations_Interface():

    def initialize(
        self,
    ) -> None:
        ...

    def initialize_model_validations(
        self,
        model_name: ModelName,
    ) -> None:
        ...

    def drop_model_validations(
        self,
        model_name: ModelName,
    ) -> None:
        ...

    def run_validations_on_create(
        self,
        model_name: ModelName,
        data: list[RecordData],
    ) -> None:
        ...

    def run_validations_on_update(
        self,
        model_name: ModelName,
        search_criteria: CriteriaStructure,
        data: RecordData,
    ) -> None:
        ...

    def run_validations_on_delete(
        self,
        model_name: ModelName,
        record_ids: list[int],
    ) -> None:
        ...
