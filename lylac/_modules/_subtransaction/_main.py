from ..._core.main import _Lylac_Core
from ..._core.modules import Subtransaction_Core
from ..._module_types import (
    RecordData,
    Many2ManyUpdatesOnCreateCallback,
    Many2ManyUpdatesOnUpdateCallback,
    ModelName,
    PosCreationCallback,
    PosUpdateCallback,
    RecordIDs,
    SubtransactionCommands,
)
from ._submodules import _Many2Many, _One2Many

class Subtransaction(Subtransaction_Core):

    def __init__(
        self,
        instance: _Lylac_Core,
    ) -> None:

        # Asignación de la instancia principal
        self._main = instance
        # Asignación de la instancia de estructura interna
        self._strc = instance._strc
        # Asignación de la instancia de compilador
        self._compiler = instance._compiler

        # Asignación de submódulos
        self._m_many2many = _Many2Many(self)
        self._m_one2many = _One2Many(self)

    def build_many2many_updates_after_create(
        self,
        model_name: ModelName,
        data: list[RecordData],
    ) -> PosCreationCallback:
        """
        ### Construcción de actualizaciones `many2many` en creación
        Este método extrae los comandos de los valores de los campos `many2many` y
        crea funciones de modificación de registros referenciados que se ejecutan
        tras la creación de los registros que los referencían.
        """

        # Inicialización de lista de transacciones por datos
        subtransactions_per_data: list[Many2ManyUpdatesOnCreateCallback] = []
        # Obtención de los nombres de campo many2many
        many2many_fields_in_model = self._strc.get_ttype_fields(model_name, 'many2many')

        # Iteración por la lista de registros
        for ( index, record ) in enumerate(data):
            # Iteración por cada campo many2many
            for many2many_field in many2many_fields_in_model:
                # SI el campo existe en las llaves de los datos del registro...
                if many2many_field in record.keys():
                    # Obtención de los comandos de transacción
                    subtransaction_commands: list[SubtransactionCommands] = record[many2many_field].copy()
                    # Se borran los datos originales
                    del record[many2many_field]

                    # Creación de las funciones de subtransacciones por campo
                    subtransactions_per_field = self._m_many2many.create_many2many_updates_for_creation_mode(
                        model_name,
                        many2many_field,
                        subtransaction_commands,
                        index,
                    )

                    # Se añade la lista de subtransacciones por campo a la lista de subtransacciones por datos
                    subtransactions_per_data += subtransactions_per_field

        # Inicialización de función de ejecución de subtransacciones
        def execute_many2many_subtransactions(created_record_ids: RecordIDs) -> None:
            # Iteración por cada subtransacción
            for subtransaction in subtransactions_per_data:
                # Ejecución de la subtransacción
                subtransaction(created_record_ids)

        return execute_many2many_subtransactions

    def build_many2many_updates_after_update(
        self,
        model_name: ModelName,
        record_ids: RecordIDs,
        data: RecordData,
    ) -> PosUpdateCallback:
        """
        ### Construcción de actualizaciones `many2many` en actualización
        Este método extrae lo comandos en los valores de los campos `many2many` y
        crea funciones de modificación de registros referenciados que se ejecutan
        tras la modificación de los registros que los referencían.
        """

        # Inicialización de lista de actualizaciones
        subtransactions_per_data: list[Many2ManyUpdatesOnUpdateCallback] = []
        # Obtención de los nombres de campos many2many del modelo
        many2many_fields = self._strc.get_ttype_fields(model_name, 'many2many')

        # Iteración por cada uno de los campos many2many contenido en el modelo
        for many2many_field in many2many_fields:
            # Si el campo existe en los datos
            if many2many_field in data.keys():
                # Obtención de los comandos de subtransacción
                subtransaction_commands: list[SubtransactionCommands] = data[many2many_field].copy()
                # Se eliminan los datos originales
                del data[many2many_field]

                # Creación de las funciones de subtransacciones por campo
                subtransactions_per_field = self._m_many2many.create_many2many_updates_for_update_mode(
                    model_name,
                    many2many_field,
                    subtransaction_commands,
                    record_ids,
                )

                # Se añade la lista de subtransacciones por campoa a la lista de subtransacciones por datos
                subtransactions_per_data += subtransactions_per_field

        # Inicialización de función de ejecución de subtransacciones
        def execute_many2many_subtransactions() -> None:
            # Iteración por cada subtransacción
            for subtransaction in subtransactions_per_data:
                # Ejecución de la subtransacción
                subtransaction()

        return execute_many2many_subtransactions

    def build_one2many_updates_after_create(
        self,
        model_name: ModelName,
        data: list[RecordData],
    ) -> PosCreationCallback:
        """
        ### Construcción de actualizaciones `many2many` en creación
        Este método extrae los comandos de los valores de los campos `many2many` y
        crea funciones de modificación de registros referenciados que se ejecutan
        tras la creación de los registros que los referencían.
        """

        # Inicialización de lista de transacciones por datos
        subtransactions_per_data: list[Many2ManyUpdatesOnCreateCallback] = []
        # Obtención de los nombres de campo many2many
        one2many_fields_in_model = self._strc.get_ttype_fields(model_name, 'one2many')
        # Iteración por la lista de registros
        for ( index, record ) in enumerate(data):
            # Iteración por cada campo many2many
            for one2many_field in one2many_fields_in_model:
                # SI el campo existe en las llaves de los datos del registro...
                if one2many_field in record.keys():
                    # Obtención de los comandos de transacción
                    subtransaction_commands: list[SubtransactionCommands] = record[one2many_field].copy()
                    # Se borran los datos originales
                    del record[one2many_field]

                    # Creación de las funciones de subtransacciones por campo
                    subtransactions_per_field = self._m_one2many.create_one2many_updates_for_creation_mode(
                        model_name,
                        one2many_field,
                        subtransaction_commands,
                        index,
                    )

                    # Se añade la lista de subtransacciones por campo a la lista de subtransacciones por datos
                    subtransactions_per_data += subtransactions_per_field

        # Inicialización de función de ejecución de subtransacciones
        def execute_one2many_subtransactions(created_record_ids: RecordIDs) -> None:
            # Iteración por cada subtransacción
            for subtransaction in subtransactions_per_data:
                # Ejecución de la subtransacción
                subtransaction(created_record_ids)

        return execute_one2many_subtransactions

    def build_one2many_updates_after_update(
        self,
        model_name: ModelName,
        record_ids: RecordIDs,
        data: RecordData,
    ) -> PosUpdateCallback:

        # Inicialización de lista de actualizaciones
        subtransactions_per_data: list[Many2ManyUpdatesOnUpdateCallback] = []
        # Obtención de los nombres de campos one2many del modelo
        one2many_fields = self._strc.get_ttype_fields(model_name, 'one2many')

        # Iteración por cada uno de los campos one2many contenido en el modelo
        for one2many_field in one2many_fields:
            # Si el campo existe en los datos
            if one2many_field in data.keys():
                # Obtención de los comandos de subtransacción
                subtransaction_commands: list[SubtransactionCommands] = data[one2many_field].copy()
                # Se eliminan los datos originales
                del data[one2many_field]

                # Creación de las funciones de subtransacciones por campo
                subtransactions_per_field = self._m_one2many.create_one2many_updates_for_update_mode(
                    model_name,
                    one2many_field,
                    subtransaction_commands,
                    record_ids,
                )

                # Se añade la lista de subtransacciones por campo a la lista de subtransacciones dpor datos
                subtransactions_per_data += subtransactions_per_field

        # Inciailización de función de ejecución de subtransacciones
        def execute_one2many_subtransactions() -> None:
            # Iteración por cada subtransacción
            for subtransaction in subtransactions_per_data:
                # Ejecución de la subtransacción
                subtransaction()

        return execute_one2many_subtransactions
