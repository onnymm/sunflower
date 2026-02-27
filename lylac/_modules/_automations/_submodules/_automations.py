from ...._contexts import AutomationContext
from ...._core.modules import Automations_Core
from ...._module_types import ModelRecordData

class _Automations():
    _automations: Automations_Core

    def __init__(
        self,
        instance: Automations_Core,
    ):

        # Asignación de la clase propietaria
        self._automations = instance

    def register_new_model(
        self,
        ctx: AutomationContext.Individual[ModelRecordData.BaseModel_],
    ) -> None:

        self._automations.register_model(ctx.data['model'])
