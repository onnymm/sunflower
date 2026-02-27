from ...._core.modules import Compute_Core
from ...._contexts import AutomationContext
from ...._module_types import ModelRecordData
class _Automations():

    def __init__(
        self,
        instance: Compute_Core,
    ) -> None:

        # Asignación de instancia propietaria
        self._compute = instance

    def register_model(
        self,
        ctx: AutomationContext.Individual[ModelRecordData.BaseModel_],
    ) -> None:

        # Obtención del nombre de modelo del modelo
        model_name = ctx.data['model']
        # Registro del modelo
        self._compute.register_model(model_name)

    def unregister_model(
        self,
        ctx: AutomationContext.Individual[ModelRecordData.BaseModel_],
    ) -> None:

        # Obtención del nombre de modelo del modelo
        model_name = ctx.data['model']
        # Registro del modelo
        self._compute.unregister_model(model_name)
