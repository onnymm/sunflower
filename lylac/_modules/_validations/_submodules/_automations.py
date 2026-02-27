from ...._contexts import AutomationContext
from ...._constants import MODEL_NAME
from ...._module_types import (
    DataPerRecord,
    ModelRecordData,
)
from ...._core.modules import Validations_Core

class _Automations():
    _validations: Validations_Core

    def __init__(
        self,
        instance: Validations_Core,
    ) -> None:

        # Asignación de instancia propietaria
        self._validations = instance
        # Asignación de instancia principal
        self._main = instance._main

    def initialize_validations(
        self,
        ctx: AutomationContext.Individual[ModelRecordData.BaseModel_],
        # params: DataPerRecord[ModelRecordData.BaseModel_],
    ) -> None:

        # Ejecución de inicialización de validaciones de modelo
        self._validations.initialize_model_validations(ctx.data['model'])

    def delete_validations(
        self,
        ctx: AutomationContext.Individual[ModelRecordData.BaseModel_],
        # params: DataPerRecord[ModelRecordData.BaseModel_],
    ) -> None:

        # Ejecución de eliminación de validaciones de modelo
        self._validations.drop_model_validations(ctx.data['model'])
