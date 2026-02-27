from ..._constants import (
    MODEL_NAME,
    ROOT_ID,
)
from ..._data import (
    DEFAULT_FIELD_TEMPLATE,
    UID_FIELDS,
)
from ..._module_types import (
    CriteriaStructure,
    ModelRecordData,
    NewRecord,
    ModelName,
)
from ._submodules import (
    _Automations,
    _Database,
    _Models,
    _Reset,
    _Validations,
)
from ..._core.modules import DDL_Core
from ..._core.main import _Lylac_Core

class DDLManager(DDL_Core):

    def __init__(
        self,
        instance: _Lylac_Core,
    ) -> None:

        # Asignación de la instancia propietaria
        self._main = instance
        # Referencia del módulo de estructura interna
        self._strc = instance._strc
        # Referencia del motor de conexión
        self._engine = instance._engine

        # Creación del submódulo para operaciones en la base de datos
        self._m_db = _Database(self)
        # Creación del submódulo para operaciones en los modelos de SQLAlchemy
        self._m_model = _Models(self)
        # Creación del submódulo para operaciones de reseteo de base de datos
        self._m_reset = _Reset(self)
        # Creación del submódulo de automatizaciones
        self._m_automations = _Automations(self)
        # Creación del submódulo de validaciones
        self._m_validations = _Validations(self)

    def new_table(
        self,
        model_name: ModelName,
    ) -> None:
        """
        ### Nueva tabla
        Este método realiza la declaración de un nuevo modelo de SQLAlchemy y realiza
        la creación de su respectiva tabla en la base de datos.
        """

        # Inicialización del modelo
        table_model = self._m_model.create_model(model_name)
        # Se crea el modelo como tabla en la base de datos
        table_model.__table__.create(self._engine)

    def new_relation(
        self,
        owner_model_name: ModelName,
        referenced_model_name: ModelName,
    ) -> None:

        # Inicialización de la tabla de relación
        relation_model = self._m_model.create_relation(owner_model_name, referenced_model_name)
        # Se crea el modelo como tabla en la base de datos
        relation_model.__table__.create(self._engine)

    def delete_relation(
        self,
        model_name: ModelName,
        field_name: str,
    ) -> None:

        # Obtención del nombre del modelo relacionado
        relation_model_name = self._strc.get_relation_model_name(model_name, field_name)
        # Obtención del modelo relacionado
        relation_model = self._strc.get_model(relation_model_name)
        # Se elimina la tabla de la base de datos
        relation_model.__table__.drop(self._engine)
        # Se elimina el modelo
        self._m_model.delete_model(relation_model_name)

    def new_field(
        self,
        model_name: ModelName,
        params: ModelRecordData.BaseModelField,
    ) -> None:

        # Obtención del modelo de SQLAlchemy
        model_model = self._strc.get_model(model_name)
        # Creación de los parámetros para ser usados en las automatizaciones
        new_field = self._m_model.build_field_atts(params)
        # Se añade la columna al modelo SQLAlchemy de la tabla
        self._m_model.add_field_to_model(model_model, new_field)
        # Se añade la columna a la tabla de la base de datos
        self._m_db.add_column(new_field)

    def delete_table(
        self,
        model_name: ModelName,
    ) -> None:

        # Obtención del modelo de SQLAlchemy
        model_model = self._strc.get_model(model_name)
        # Se elimina la tabla de la base de datos
        model_model.__table__.drop(self._engine)
        # Se elimina el modelo
        self._m_model.delete_model(model_name)

    def delete_field(
        self,
        model_name: ModelName,
        field_name: str,
    ) -> None:

        # Obtención de la ID del modelo
        [ model_id ] = self._main.search(ROOT_ID, MODEL_NAME.BASE_MODEL, [('model', '=', model_name)])
        # Creación de criterio de búsqueda para encontrar todos los campos pertenientes al modelo
        criteria: CriteriaStructure = [
            '&',
                '&',
                    '&',
                        ('model_id', '=', model_id),
                        ('name', '!=', field_name),
                    ('name', 'not in', ['id', 'name', 'create_date', 'write_date']),
                ('ttype', 'not in', ['one2many', 'many2many']),
        ]

        # Se obtienen los datos de los registros a excepción del campo eliminado
        fields_data: list[ModelRecordData.BaseModelField] = self._main.search_read(
            ROOT_ID,
            MODEL_NAME.BASE_MODEL_FIELD,
            criteria,
            output_format= 'dict',
            only_ids_in_relations= True
        )

        # Se crean las instancias de campos para ser añadidas
        fields_atts = [ self._m_model.build_field_atts(field) for field in fields_data ]
        # Obtención del nombre de la tabla
        table_name = self._strc.get_table_name(model_name)
        # Se elimina la columna de la tabla de base de datos
        self._m_db.drop_column(table_name, field_name)
        # Se elimina el modelo de SQLAlchemy
        self._m_model.delete_model(model_name)
        # Se vuelve a crear el modelo
        table_model = self._m_model.create_model(table_name)

        # Se añaden los campos que tenía registrados
        for field in fields_atts:
            self._m_model.add_field_to_model(table_model, field)

    def add_default_to_model(
        self,
        model_id: int,
        field_names: list[str] = [],
    ) -> None:

        # Inicialización de los campos plantilla del modelo
        model_fields_template = []
        # Se añaden los campos UID
        model_fields_template = field_names + UID_FIELDS
        # Inicialización de la lista de datos a retornar
        fields_data: list[NewRecord.ModelField] = []

        # Creación de los datos por cada nombre de campo
        for field_name in model_fields_template:

            # Se obtiene una copia de la plantilla de información
            field_data = self.build_default_field(field_name, model_id)
            # Se añaden los datos del campo a la lista de datos a retornar
            fields_data.append(field_data)

        # Se crea la información de los campos
        self._main.create(ROOT_ID, MODEL_NAME.BASE_MODEL_FIELD, fields_data)

    def build_default_field(
        self,
        field_name: str,
        model_id: int,
    ) -> NewRecord.ModelField:

        # Obtención de los datos prestablecidos de la definición del campo
        field_template = DEFAULT_FIELD_TEMPLATE[field_name].copy()
        # Se asigna la ID del modelo
        field_template['model_id'] = model_id

        return field_template
