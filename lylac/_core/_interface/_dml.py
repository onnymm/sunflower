from ..._module_types import (
    CriteriaStructure,
    RecordData,
    ItemOrList,
    ModelName,
)

class DML_Interface():

    def create(
        self,
        model_name: ModelName,
        data: list[RecordData],
    ) -> list[int]:
        ...

    def update_where(
        self,
        model_name: ModelName,
        search_criteria: CriteriaStructure,
        data: RecordData,
    ) -> bool:
        ...

    def delete(
        self,
        model_name: ModelName,
        record_ids: ItemOrList[int]
    ) -> bool:
        ...
