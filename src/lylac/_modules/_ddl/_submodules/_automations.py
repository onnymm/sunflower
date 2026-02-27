from ...._constants import (
    MODEL_NAME,
    FIELD_LABEL,
    FIELD_NAME,
)
from ...._core.modules import DDL_Core
from ...._contexts import AutomationContext
from ...._data import BASE_FIELDS_TEMPLATE
from ...._module_types import ModelRecordData

class _Automations():
    _ddl: DDL_Core

    def __init__(
        self,
        instance: DDL_Core,
    ) -> None:

        # Asignación de la instancia propietaria
        self._ddl = instance
        # Referencia de la instancia principal
        self._main = instance._main
        # Referencia del motor de conexión
        self._engine = instance._main._engine
        # Referencia del módulo de modelos
        self._model = instance._m_model
        # Referencia de la estructura interna de tablas
        self._strc = instance._main._strc

    def create_table(
        self,
        ctx: AutomationContext.Individual[ModelRecordData.BaseModel_],
    ) -> None:

        # Obtención del nombre del modelo creado
        model_name = ctx.data['name']
        # Creación de la tabla en la base de datos
        self._ddl.new_table(model_name)

    def create_column(
        self,
        ctx: AutomationContext.Individual[ModelRecordData.BaseModelField],
        # params: DataPerRecord[ModelRecordData.BaseModelField],
    ) -> None:

        # Obtención de la ID del modelo del campo creado
        model_id = ctx.data['model_id']
        # Obtención del nombre del modelo
        model_name = ctx.get_value(MODEL_NAME.BASE_MODEL, model_id, 'model')
        # Se añade el campo a la tabla indicada
        self._ddl.new_field(model_name, ctx.data)

    def delete_table(
        self,
        params: AutomationContext.Individual[ModelRecordData.BaseModel_],
    ) -> None:

        # Obtención del nombre del modelo
        model_name = params.data['model']
        # Ejecución del método del módulo principal
        self._ddl.delete_table(model_name)

    def delete_column(
        self,
        ctx: AutomationContext.Individual[ModelRecordData.BaseModelField]
        # params: DataPerRecord[ModelRecordData.BaseModelField],
    ) -> None:

        # Obtención de la ID del modelo del campo creado
        model_id = ctx.data['model_id']
        # Obtención del nombre del modelo
        model_name = ctx.get_value(MODEL_NAME.BASE_MODEL, model_id, 'model')
        # Obtención del nombre del campo
        field_name = ctx.data['name']
        # Ejecución del método del módulo principal
        self._ddl.delete_field(model_name, field_name)

    def create_relation_table(
        self,
        ctx: AutomationContext.Individual[ModelRecordData.BaseModelField],
        # params: DataPerRecord[ModelRecordData.BaseModelField],
    ) -> None:

        # Nombre del modelo propietario
        model_name = ctx.get_value(MODEL_NAME.BASE_MODEL, ctx.data['model_id'], 'model')
        # Nombre del modelo referenciado
        related_model_name = ctx.get_value(MODEL_NAME.BASE_MODEL, ctx.data['related_model_id'], 'model')
        # Creación de la tabla de relación
        self._ddl.new_relation(model_name, related_model_name)

    def delete_relation_table(
        self,
        ctx: AutomationContext.Individual[ModelRecordData.BaseModelField],
        # params: DataPerRecord[ModelRecordData.BaseModelField],
    ) -> None:

        # Nombre del modelo propietario
        model_name = ctx.get_value(MODEL_NAME.BASE_MODEL, ctx.data['model_id'], 'model')
        # Nombre del campo
        field_name = ctx.data['name']

        # Se elimina la tabla de relación
        self._ddl.delete_relation(model_name, field_name)

    def create_base_fields(
        self,
        ctx: AutomationContext.Individual[ModelRecordData.BaseModel_],
        # params: DataPerRecord[ModelRecordData.BaseModel_],
    ) -> None:

        # Inicialización de los datos
        fields_data: list[ModelRecordData.BaseModelField] = []

        # Se crea la información
        for base_field in BASE_FIELDS_TEMPLATE:
            # Se crea una copia de la información
            field_data = base_field.copy()
            # Se añade la ID del modelo a vincular
            field_data['model_id'] = ctx.data['id']
            # Se añade la información a la lista de datos
            fields_data.append(field_data)

        # Se crean los registros en la tabla de campos
        ctx.create(MODEL_NAME.BASE_MODEL_FIELD, fields_data)

    def add_preset_fields(
        self,
        ctx: AutomationContext.Individual[ModelRecordData.BaseModel_],
        # params: DataPerRecord[ModelRecordData.BaseModel_],
    ) -> None:

        # Obtención de la ID del modelo
        model_id = ctx.data['id']
        # Se añaden los campos predeterminados
        self._ddl.add_default_to_model(model_id)

    def update_selection_values_on_create(
        self,
        ctx: AutomationContext.Individual[ModelRecordData.BaseModelFieldSelection],
        # params: DataPerRecord[ModelRecordData.BaseModelFieldSelection],
    ) -> None:

        # Obtención de la ID del campo propietario
        field_id = ctx.data['field_id']
        # Obtención de la ID del modelo propietario
        model_id = ctx.get_value(MODEL_NAME.BASE_MODEL_FIELD, field_id, 'model_id')
        # Obtención del nombre del modelo propietario
        model_name = ctx.get_value(MODEL_NAME.BASE_MODEL, model_id, 'model')
        # Obtención del nombre del campo propietario
        field_name = ctx.get_value(MODEL_NAME.BASE_MODEL_FIELD, field_id, 'name')

        # Obtención de los valores de selección
        selection_values = (
            ctx.search_read(
                MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
                [('field_id', '=', field_id)],
                ['name'],
                output_format= 'dataframe',
            )
            ['name']
            .to_list()
        )

        # Actualización de los valores de selección
        self._strc.update_selection_values(
            model_name,
            field_name,
            selection_values,
        )

    def update_selection_values_on_delete(
        self,
        ctx: AutomationContext.Individual[ModelRecordData.BaseModelFieldSelection],
        # params: DataPerRecord[ModelRecordData.BaseModelFieldSelection],
    ) -> None:

        # Obtención de la ID del campo propietario
        field_id = ctx.data['field_id']
        # Obtención de la ID del modelo propietario
        model_id = ctx.get_value(MODEL_NAME.BASE_MODEL_FIELD, field_id, 'model_id')
        # Obtención del nombre del modelo propietario
        model_name = ctx.get_value(MODEL_NAME.BASE_MODEL, model_id, 'model')
        # Obtención del nombre del campo propietario
        field_name = ctx.get_value(MODEL_NAME.BASE_MODEL_FIELD, field_id, 'name')

        # Obtención de los valores de selección
        selection_values = (
            ctx.search_read(
                MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
                [
                    '&',
                        ('field_id', '=', field_id),
                        ('id', '!=', ctx.data['id']),
                ],
                ['name'],
                output_format= 'dataframe',
            )
            ['name']
            .to_list()
        )

        # Actualización de los valores de selección
        self._strc.update_selection_values(
            model_name,
            field_name,
            selection_values,
        )

    def initialize_display_name_field(
        self,
        ctx: AutomationContext.Individual[ModelRecordData.BaseModel_],
    ) -> None:

        # Obtención de la ID del modelo
        model_id = ctx.data['id']
        # Obtención del nombre de modelo del modelo
        model_model_name = ctx.data['model']
        # Creación del campo computado sin función
        ctx.create(
            MODEL_NAME.BASE_MODEL_FIELD,
            {
                'name': FIELD_NAME.DISPLAY_NAME,
                'label': FIELD_LABEL.DISPLAY_NAME,
                'ttype': 'char',
                'model_id': model_id,
                'state': 'base',
                'is_computed': True,
            },
        )
        # Registro de campo en la estructura
        self._main._strc.register_field(
            model_model_name,
            FIELD_NAME.DISPLAY_NAME,
            'char',
            None,
            None,
            [],
            True,
        )
