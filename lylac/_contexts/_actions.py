from typing import Generic, Callable
from .._core.main import _Lylac_Core
from lylac._module_types import (
    _T,
    CriteriaStructure,
    RecordData,
    DataOutput,
    OutputOptions,
    ModelName,
    RecordValue,
)

class ActionContext(Generic[_T]):
    data: _T
    """
    Datos del registro en el que se ejecuta la acción.
    """
    _main: _Lylac_Core

    def __init__(
        self,
        instance: _Lylac_Core,
        data: _T,
        user_id: int,
    ) -> None:

        self.data = data
        self._main = instance
        self._user_id = user_id

    def reset_password(
        self,
        user_id_to_reset_password: int,
    ) -> bool:

        return self._main.reset_password(
            self._user_id,
            user_id_to_reset_password,
        )

    def create(
        self,
        model_name: ModelName,
        data: RecordData | list[RecordData],
    ) -> list[int]:

        return self._main.create(
            self._user_id,
            model_name,
            data,
        )

    def search(
        self,
        model_name: ModelName,
        search_criteria: CriteriaStructure = [],
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[int]:

        return self._main.search(
            self._user_id,
            model_name,
            search_criteria,
            offset,
            limit,
        )

    def get_value(
        self,
        model_name: ModelName,
        record_id: int,
        field_name: str,
    ) -> RecordValue:

        return self._main.get_value(
            self._user_id,
            model_name,
            record_id,
            field_name,
        )

    def get_values(
        self,
        model_name: ModelName,
        record_id: int,
        fields: list[str],
    ) -> tuple:

        return self._main.get_values(
            self._user_id,
            model_name,
            record_id,
            fields,
        )

    def search_count(
        self,
        model_name: ModelName,
        search_criteria: CriteriaStructure = [],
    ) -> int:

        self._main.search_count(
            self._user_id,
            model_name,
            search_criteria,
        )

    def search_read(
        self,
        model_name: ModelName,
        search_criteria: CriteriaStructure = [],
        fields: list[str] = [],
        offset: int | None = None,
        limit: int | None = None,
        sortby: str | list[str] | None = None,
        ascending: bool | list[bool] = True,
        output_format: OutputOptions | None = None,
    ) -> DataOutput:
        
        return self._main.search_read(
            self._user_id,
            model_name,
            search_criteria,
            fields,
            offset,
            limit,
            sortby,
            ascending,
            output_format,
            only_ids_in_relations= True,
        )

    def update(
        self,
        model_name: ModelName,
        record_ids: int | list[int],
        data: RecordData,
    ) -> bool:

        self._main.update(
            self._user_id,
            model_name,
            record_ids,
            data,
        )

    def delete(
        self,
        model_name: ModelName,
        record_ids: int | list[int]
    ) -> bool:

        return self._main.delete(
            self._user_id,
            model_name,
            record_ids,
        )

ActionCallback = Callable[[ActionContext], bool]
