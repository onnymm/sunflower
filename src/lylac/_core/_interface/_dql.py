from typing import Optional
import pandas as pd
from ..._module_types import (
    CriteriaStructure,
    ItemOrList,
    ModelName,
    OutputOptions,
    RecordValue,
)

class DQL_Interface():

    def search(
        self,
        model_name: ModelName,
        search_criteria: CriteriaStructure,
        offset: Optional[int],
        limit: Optional[int],
    ) -> list[int]:
        ...

    def read(
        self,
        model_name: ModelName,
        record_ids: ItemOrList[int],
        fields: list[str],
        sortby: ItemOrList[str],
        ascending: ItemOrList[bool],
        output_format: Optional[OutputOptions],
        only_ids_in_relations: bool,
    ) -> pd.DataFrame | list[dict[str, RecordValue]]:
        ...

    def search_read(
        self,
        model_name: ModelName,
        search_criteria: CriteriaStructure = [],
        fields: list[str] = [],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sortby: Optional[ ItemOrList[str] ] = None,
        ascending: ItemOrList[bool] = True,
        output_format: Optional[OutputOptions] = None,
        only_ids_in_relations: bool = False,
    ) -> pd.DataFrame | dict[str, RecordValue]:
        ...

    def search_count(
        self,
        model_name: ModelName,
        search_criteria: CriteriaStructure,
    ) -> int:
        ...
