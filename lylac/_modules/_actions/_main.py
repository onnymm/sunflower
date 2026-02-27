from ..._contexts._actions import (
    ActionContext,
    ActionCallback,
)
from ..._core.main import _Lylac_Core
from ..._core.modules import Actions_Core
from ..._module_types import ModelName
from ._module_types import ActionsHub
from ._submodules import _Automations


class Actions(Actions_Core):
    _hub: ActionsHub

    def __init__(
        self,
        instance: _Lylac_Core,
    ) -> None:

        # Asignación de instancia principal
        self._main = instance
        # Inicialización del submódulo de automatizaciones
        self._m_automations = _Automations(self)
        # Inicialización del módulo
        self._initialize()

    def register_action(
        self,
        model_name: ModelName,
        action_name: str,
        action_callback: ActionCallback,
    ) -> None:

        # Registro de la acción
        self._hub[model_name][action_name] = action_callback

    def run_action(
        self,
        user_id: int,
        model_name: ModelName,
        action_name: str,
        record_id: int,
    ) -> None:

        # Obtención de los datos del registro
        [ record_data ] = self._main.read(user_id, model_name, record_id, output_format= 'dict')
        # Obtención de la función de acción a ejecutar
        action_callback = self._hub[model_name][action_name]
        # Inicialización del objeto de contexto
        ctx = ActionContext(
            instance= self._main,
            data= record_data,
            user_id= user_id
        )
        # Ejecución de la acción
        action_callback(ctx)

    def _initialize(
        self,
    ) -> None:

        # Inicialización del núcleo de automatizaciones
        self._hub: ActionsHub = {}
        # Obtención de los nombres de modelos iniciales
        model_names = self._main._strc.get_model_names()
        # Se crean los diccionarios de automatizaciones para cada modelo
        for model_name in model_names:
            self._hub[model_name] = {}

    def register_model(
        self,
        model_name: ModelName,
    ) -> None:

        # Se crea el diccionario de automatizaciones para el nuevo modelo
        self._hub[model_name] = {}

    def unregister_model(
        self,
        model_name: ModelName,
    ) -> None:

        # Se elimina el diccionario de automatizaciones del modelo
        del self._hub[model_name]
