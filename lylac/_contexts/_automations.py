from typing import Generic, Callable
from lylac._module_types import (
    _T,
    CriteriaStructure,
    RecordData,
    DataOutput,
    OutputOptions,
    ModelName,
    RecordValue,
)
from .._core.main import _Lylac_Core

class _BaseContext():
    _main: _Lylac_Core
    """
    Instancia principal.
    """

    def __init__(
        self,
        instance: _Lylac_Core,
        data,
        model_name: ModelName,
        user_id: int,
    ) -> None:

        self.data = data
        self.model_name = model_name
        """
        Modelo donde se ejecuta la acción.
        """
        self._user_id = user_id
        """
        Usuario que ejecuta la acción.
        """
        self._main = instance

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

class _Individual(_BaseContext, Generic[_T]):
    data: _T
    """
    Diccionario de datos del registro en el modelo correspondiente.
    """

class _Group(_BaseContext, Generic[_T]):
    data: list[_T]
    """
    Lista de diccionarios de datos de registros en el modelo correspondiente.
    """

class AutomationContext:
    Individual = _Individual
    Group = _Group

AutomationCallback = Callable[[AutomationContext.Individual | AutomationContext.Group], None]
