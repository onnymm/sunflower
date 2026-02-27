from typing import Callable
from ..._module_types import (
    _T,
    RecordData,
    ItemOrList,
    ModelName,
)

RecordIds = list[int]
PosCreationCallback = Callable[[RecordIds], None]
PosUpdateCallback = Callable[[], None]
FieldName = str
RecordMany2ManyData = dict[FieldName, RecordIds]

class Preprocess_Interface():

    def convert_to_list(
        self,
        data: ItemOrList[_T],
    ) -> list[_T]:
        ...

    def process_data_on_create(
        self,
        user_id: int,
        model_name: ModelName,
        data: RecordData | list[RecordData],
    ) -> PosCreationCallback:
        ...

    def process_data_on_update(
        self,
        user_id: int,
        model_name: ModelName,
        record_ids: RecordIds,
        data: RecordData,
    ) -> Callable[[], None]:
        ...
