from ..._constants import FIELD_NAME
from ..._module_types import (
    CriteriaStructure,
    AutomationMethodName,
    ModelName,
    UpsertTransactionName,
    WriteTransactionName,
)

class Automations_Interface():

    def register_automation(
        self,
        model_name: ModelName,
        transaction: WriteTransactionName,
        callback, # TODO resolver tipado
        fields: list[str] = [FIELD_NAME.ID,],
        criteria: CriteriaStructure = [],
        method: AutomationMethodName = 'record'
    ) -> None:
        ...

    def register_model(
        self,
        model_name: ModelName,
    ) -> None:
        ...

    def run_after_transaction(
        self,
        model_name: ModelName,
        transaction: UpsertTransactionName,
        record_ids: list[int],
        user_id: int,
    ) -> None:
        ...

    def generate_before_transaction(
        self,
        model_name: ModelName,
        record_ids: list[int],
        user_id: int,
    ):
        ...

    def create_preset_automations(
        self,
    ) -> None:
        ...
