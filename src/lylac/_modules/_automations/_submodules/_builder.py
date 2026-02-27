from ...._constants import ROOT_ID
from ...._contexts import AutomationContext
from ...._core.modules import Automations_Core
from ...._core.submods.automations import _Builder_Interface
from .._module_types import ProgrammedAutomation
from ...._module_types import (
    ModelName,
    RecordData,
)
from .._module_types import (
    CompiledDeletionAutomation,
    CompiledModificationAutomation,
)

class _Builder(_Builder_Interface):
    _automations: Automations_Core

    def __init__(
        self,
        instance: Automations_Core,
    ):

        # Asignación de la instancia propietaria
        self._automations = instance
        # Asignación de la instancia principal
        self._main = instance._main

    def build_runable_modification_automation(
        self,
        model_name: ModelName,
        found_ids: list[int],
        autom_data: ProgrammedAutomation,
        user_id: int,
    ) -> CompiledModificationAutomation:

        # Obtención de mapa de información de los registros
        mapped_data = self._get_records_data_for_automation(
            model_name,
            found_ids,
            autom_data,
        )

        # Inicialización de la función para ejecución de las automatizaciones
        def automation_to_execute():

            # Obtención de la función de automatización a ejecutar
            automation_callback = autom_data.callback

            # Si el tipo de ejecución es por registro
            if autom_data.execution == 'record':
                # Ejecución de automatización por registro
                for record_id in found_ids:
                    # Obtención del registro a usar para entrada de argumentos a la automatización
                    input_record = mapped_data[record_id]
                    # Creación del contexto a ingresar a la función automatización
                    ctx = AutomationContext.Individual(
                        self._main,
                        input_record,
                        model_name,
                        user_id,
                    )
                    # Ejecución de la automatización
                    automation_callback(ctx)
                    # Notificación de ejecución de la automatización
                    print(f'La automatización [{automation_callback.__name__}] se ha ejecutado con el registro {record_id} del modelo [{model_name}]')

            # Ejecución por toda la lista de registros provistos
            else:
                # Obtención de los datos a proporcionar
                data = list( mapped_data.values() )
                # Creación del contexto a ingresar a la función automatización
                ctx = AutomationContext.Group(
                    self._main,
                    data,
                    model_name,
                    user_id,
                )
                # Ejecución de la automatización
                automation_callback(ctx)

        # Retorno de la función para ejecutar las automatizaciones
        return automation_to_execute

    def build_runable_deletion_automation(
        self,
        model_name: ModelName,
        found_ids: list[int],
        autom_data: ProgrammedAutomation,
        user_id: int,
    ) -> CompiledDeletionAutomation:

        # Obtención de mapa de información de los registros
        mapped_data = self._get_records_data_for_automation(
            model_name,
            found_ids,
            autom_data,
        )

        # Inicialización de la función para ejecución de las automatizaciones
        def automation_to_execute(deleted_ids: list[int]):

            # Se inicializa una lista con las IDs que solo aplican
            applyable_ids = list( set(found_ids) & set(deleted_ids) )

            # Si el tipo de ejecución es por registro
            if autom_data.execution == 'record':
                # Ejecución de automatización por registro
                for record_id in applyable_ids:
                    # Obtención del registro a usar para entrada de argumentos a la automatización
                    record_data = mapped_data[record_id]
                    # Creación del contexto a ingresar a la función automatización
                    ctx = AutomationContext.Individual(
                        self._main,
                        record_data,
                        model_name,
                        user_id,
                    )
                    # Ejecución de la automatización
                    autom_data.callback(ctx)
            # Ejecución por toda la lista de registros provistos
            else:
                # Obtención de los datos a proporcionar
                data = list( record_data.values() )
                # Creación del contexto a ingresar a la función automatización
                ctx = AutomationContext.Group(
                    self._main,
                    data,
                    model_name,
                    user_id,
                )
                # Ejecución de la automatización
                autom_data.callback(ctx)

        return automation_to_execute

    def _get_records_data_for_automation(
        self,
        model_name: ModelName,
        found_ids: list[int],
        autom_data: ProgrammedAutomation,
    ) -> dict[int, RecordData]:

        # Inicialización de datos de registros mapeados
        mapped_data: dict[int, RecordData] = {}
        # Se obtienen los datos de los registros
        records_data = self._main.read(
            ROOT_ID,
            model_name,
            found_ids,
            autom_data.fields,
            output_format= 'dict',
            only_ids_in_relations= True,
        )

        # Mapeo de datos de registros
        for record_data in records_data:
            # Se indexan los datos de cada registro por medio de su ID
            mapped_data[ record_data['id'] ] = record_data

        return mapped_data

