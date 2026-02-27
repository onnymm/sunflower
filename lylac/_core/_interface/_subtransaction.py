from ..._module_types import (
    RecordData,
    ModelName,
    PosCreationCallback,
    PosUpdateCallback,
    RecordIDs,
)

class Subtransaction_Interface():

    def build_many2many_updates_after_create(
        self,
        model_name: ModelName,
        data: list[RecordData],
    ) -> PosCreationCallback:
        ...

    def build_many2many_updates_after_update(
        self,
        model_name: ModelName,
        record_ids: RecordIDs,
        data: RecordData,
    ) -> PosUpdateCallback:
        ...

    def build_one2many_updates_after_create(
        self,
        model_name: ModelName,
        data: list[RecordData],
    ) -> PosCreationCallback:
        ...

    def build_one2many_updates_after_update(
        self,
        model_name: ModelName,
        record_ids: RecordIDs,
        data: RecordData,
    ) -> PosUpdateCallback:
        ...
