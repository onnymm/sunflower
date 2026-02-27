from ..._constants import (
    FIELD_NAME,
    ROOT_ID,
)
from ..._contexts import AutomationCallback
from ..._core.modules import Automations_Core
from ..._core.main import _Lylac_Core
from ..._data import PRESET_AUTOMATIONS
from ..._module_types import (
    AutomationModel,
    CriteriaStructure,
    AutomationMethodName,
    ModelName,
    UpsertTransactionName,
    WriteTransactionName,
)
from ._module_types import (
    AutomationsHub,
    ProgrammedAutomation,
    CompiledDeletionAutomation,
    CompiledModificationAutomation,
)
from ._submodules import (
    _Automations,
    _Builder,
)

class Automations(Automations_Core):

    def __init__(
        self,
        instance: _Lylac_Core,
    ) -> None:

        # Asignación de la instancia principal
        self._main = instance
        # Referencia del módulo de estructura interna
        self._strc = instance._strc
        # Inicialización del submódulo de automatizaciones
        self._m_automations = _Automations(self)
        # inicialización del submódulo de constructor
        self._m_builder = _Builder(self)

        # Inicialización del núcleo de datos
        self._initialize_hub()

    def register_automation(
        self,
        model_name: ModelName,
        transaction: WriteTransactionName,
        callback: AutomationCallback,
        fields: list[str] = [FIELD_NAME.ID,],
        criteria: CriteriaStructure = [],
        method: AutomationMethodName = 'record'
    ) -> None:

        # Creación de la automatización programada
        autom_data = ProgrammedAutomation(
            criteria= criteria,
            callback= callback,
            fields= fields,
            execution= method,
        )

        # Se añade la automatización programada en la transacción correspondiente de su tabla
        self._hub[model_name][transaction].append(autom_data)

    def register_model(
        self,
        model_name: ModelName,
    ) -> None:

        self._hub[model_name] = {
            'create': [],
            'update': [],
            'delete': [],
        }

    def run_after_transaction(
        self,
        model_name: ModelName,
        transaction: UpsertTransactionName,
        record_ids: list[int],
        user_id: int,
    ) -> None:

        # Se inicializa la lista de automatizaciones a ejecutar
        automations_to_run: list[CompiledModificationAutomation] = []

        # Iteración por cada automatización programada
        for autom_data in self._hub[model_name][transaction]:
            # Obtención de las IDs de los registros aplicables para la automatización
            applyable_ids = self._find_applyable_records_for_automation(model_name, record_ids, autom_data )

            # Si existen IDs para ejecutar la automatización
            if len(applyable_ids):
                # Inicialización de la función que ejecuta la automatización únicamente con las IDs encontradas
                automation_to_execute = self._m_builder.build_runable_modification_automation(
                    model_name,
                    applyable_ids,
                    autom_data,
                    user_id,
                )
                # Se añade la función preparada
                automations_to_run.append(automation_to_execute)

        # Ejecución de las automatizaciones
        for callback in automations_to_run:
            callback()

    def generate_before_transaction(
        self,
        model_name: ModelName,
        record_ids: list[int],
        user_id: int,
    ):

        # Se inicializa la lista de automatizaciones a ejecutar
        automations_to_run: list[CompiledDeletionAutomation] = []

        # Iteración por cada automatización programada
        for autom_data in self._hub[model_name]['delete']:
            # Obtención de las IDs de los registros aplicables para la automatización
            applyable_ids = self._find_applyable_records_for_automation(model_name, record_ids, autom_data)

            # Si existen IDs para ejecutar la automatización
            if len(applyable_ids):

                # Inicialización de la función que ejecuta la automatización únicamente con las IDs encontradas
                automation_to_execute = self._m_builder.build_runable_deletion_automation(
                    model_name,
                    applyable_ids,
                    autom_data,
                    user_id,
                )

                # Se añade la función preparada
                automations_to_run.append(automation_to_execute)

        # Inicialización de función ejecutable
        def run_automations_after_deletion(deleted_ids: list[int]) -> None:
            for callback in automations_to_run:
                callback(deleted_ids)

        # Retorno de función de función ejecutable
        return run_automations_after_deletion

    def create_preset_automations(
        self,
    ) -> None:

        # Registro de las automatizaciones precargadas
        for automation in [ AutomationModel(**data) for data in PRESET_AUTOMATIONS ]:

            # Obtención del módulo que contiene la automatización
            submodule = getattr(self._main, automation.submodule)
            # Obtención de la instancia de automatizaciones del submódulo
            autom_extension = getattr(submodule, '_m_automations')
            # Obtención de la función a registrar como automatización
            callback: AutomationCallback = getattr(autom_extension, automation.callback)

            # Registro de la automatización
            self.register_automation(
                automation.model,
                automation.transaction,
                callback,
                automation.fields,
                automation.criteria,
                automation.method
            )

    def _initialize_hub(
        self,
    ) -> None:

        # Inicialización de estructura central de automatizaciones
        self._hub: AutomationsHub = {}
        # Obtención de los nombres de modelos registrados
        registered_model_names = self._strc.get_model_names()
        # Iteración por cada nombre de tabla existente en la base de datos
        for model_name in registered_model_names:
            # Creación de desencadenantes de automatización vacíos
            self.register_model(model_name)

    def _find_applyable_records_for_automation(
        self,
        model_name: ModelName,
        record_ids: list[int],
        autom_data: ProgrammedAutomation,
    ) -> list[int]:

        # Obtención del criterio de evaluación de la automatización programada
        automation_criteria = autom_data.criteria
        # Obtención del criterio de búsqueda segmentado solo por las IDs de registros a evaluar
        computed_criteria = self._compute_automation_criteria(record_ids, automation_criteria)
        # Se filtran las IDs por el criterio de búsqueda computado
        found_ids = self._main.search(ROOT_ID, model_name, computed_criteria)

        return found_ids

    def _compute_automation_criteria(
        self,
        record_ids: list[int],
        autom_criteria: CriteriaStructure
    ) -> CriteriaStructure:

        # Si existe un criterio a cumplir se hace una conjunción con la lista de IDs de registros encontradas
        if len(autom_criteria):
            return self._main.and_(
                [(FIELD_NAME.ID, 'in', record_ids)],
                autom_criteria
            )
        # Si no existe un criterio a cumplir se crea un criterio de solo las IDs de registros encontradas
        else:
            return [(FIELD_NAME.ID, 'in', record_ids)]
