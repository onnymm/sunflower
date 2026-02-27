from ...._contexts import AutomationContext
from ...._core.modules import Actions_Core
from ...._module_types import ModelRecordData

class _Automations():
    _actions: Actions_Core

    def __init__(
        self,
        instance: Actions_Core,
    ):

        # Asignación de la clase propietaria
        self._actions = instance

    def register_model(
        self,
        ctx: AutomationContext.Individual[ModelRecordData.BaseModel_],
    ) -> None:

        # Obtención del nombre del modelo
        model_name = ctx.data['model']

        # Registro del nombre del modelo
        self._actions.register_model(model_name)

    def unregister_model(
        self,
        ctx: AutomationContext.Individual[ModelRecordData.BaseModel_],
    ) -> None:

        # Obtención del nombre del modelo
        model_name = ctx.data['model']

        # Eliminación del modelo
        self._actions.unregister_model(model_name)
