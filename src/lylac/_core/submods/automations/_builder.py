from .._typing._automations import (
    ProgrammedAutomation,
    CompiledDeletionAutomation,
    CompiledModificationAutomation,
)
from ...._module_types import (
    ModelName,
    RecordData,
)

class _Builder_Interface():

    def build_runable_modification_automation(
        self,
        model_name: ModelName,
        found_ids: list[int],
        autom_data: ProgrammedAutomation,
        user_id: int,
    ) -> CompiledModificationAutomation:
        ...

    def build_runable_deletion_automation(
        self,
        model_name: ModelName,
        found_ids: list[int],
        autom_data: ProgrammedAutomation,
        user_id: int,
    ) -> CompiledDeletionAutomation:
        ...

    def _get_records_data_for_automation(
        self,
        model_name: ModelName,
        found_ids: list[int],
        autom_data: ProgrammedAutomation,
    ) -> dict[int, RecordData]:
        ...
