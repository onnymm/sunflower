from typing import Optional
from sqlalchemy.orm.decl_api import DeclarativeBase
from ..._core.main import _Lylac_Core
from ..._core.modules import Structure_Core
from ..._data import FIELDS_ATTS
from ..._module_types import (
    ModelName,
    TTypeName,
)
from ._submodules import (
    _Automations,
    _RawORM,
)

class Structure(Structure_Core):

    def __init__(
        self,
        instance: _Lylac_Core
    ) -> None:

        # Asignación de instancia principal
        self._main = instance

        # Inicialización del módulo de ORM crudo
        self._m_orm = _RawORM(self)
        # Inicialización del módulo de automatizaciones
        self._m_automations = _Automations(self)

        # Inicialización de la estructura de tablas y atributos de campos
        self._initialize()

    def register_table(
        self,
        model_model: type[DeclarativeBase]
    ) -> None:

        # Obtención del nombre de la tabla
        table_name = self.get_table_name(model_model)
        # Obtención del nombre del modelo
        model_name = table_name.replace('_', '.')
        # Se registra el modelo de la tabla en el diccionario de modelos
        self.models[model_name] = self._initialize_model_properties(model_model)
        # Registro de las propiedades de los campos de la tabla
        self._register_table_fields_atts(model_name)

    def unregister_table(
        self,
        model_name: ModelName,
    ) -> None:

        # Obtención del modelo de la tabla
        table_model = self.get_model(model_name)
        # Se borra el modelo
        del table_model
        # Se borra la llave y valor del diccionario de modelos
        del self.models[model_name]

    def register_field(
        self,
        model_name: ModelName,
        field_name: str,
        ttype: TTypeName,
        related_model: Optional[str],
        related_field: Optional[str],
        selection_values: list[str] = [],
        is_computed: bool = False
    ) -> None:

        # Si el nombre del campo no existe...
        if field_name not in self.models[model_name]['fields'].keys():
            # Se crea el diccionario para mapear los atributos del campo
            self.models[model_name]['fields'][field_name] = {}

        # Asignación de valores
        self.models[model_name]['fields'][field_name]['ttype'] = ttype
        self.models[model_name]['fields'][field_name]['related_model'] = related_model
        self.models[model_name]['fields'][field_name]['related_field'] = related_field
        self.models[model_name]['fields'][field_name]['selection_values'] = selection_values
        self.models[model_name]['fields'][field_name]['is_computed'] = is_computed

    def unregister_field(
        self,
        model_name: ModelName,
        field_name: str,
    ) -> None:

        # Eliminación del registro
        del self.models[model_name]['fields'][field_name]

    def register_relation(
        self,
        model_model: type[DeclarativeBase],
    ) -> None:

        # Obtención del nombre de la tabla
        table_name = self.get_table_name(model_model)
        # Obtención del nombre del modelo
        model_name = table_name.replace('_rel_', '_rel.').replace('__', '.')
        # Se registra el modelo de la tabla en el diccionario de modelos
        self.models[model_name] = self._initialize_model_properties(model_model)

    def update_selection_values(
        self,
        model_name: ModelName,
        field_name: str,
        selection_values: list[str],
    ) -> None:

        # Asignación de los valores de selección
        self.models[model_name]['fields'][field_name]['selection_values'] = selection_values

    def get_model(
        self,
        model_name: ModelName,
    ) -> type[DeclarativeBase]:

        return self.models[model_name]['model']

    def get_relation_model(
        self,
        model_name: ModelName,
        field_name: str,
    ) -> type[DeclarativeBase]:

        # Obtención del nombre del modelo de relación
        relation_model_name = self.get_relation_model_name(model_name, field_name)
        # Obtención del modelo
        relation_model = self.get_model(relation_model_name)

        return relation_model

    def get_model_names(
        self,
    ) -> list[str]:

        # Obtención de los nombres de modelos registrados en la estructura
        registered_model_names = list( self.models.keys() )

        return registered_model_names

    def get_model_field_names(
        self,
        model_name: ModelName,
    ) -> list[str]:

        # Obtención de los nombres de campos existentes del modelo especificado
        field_names = list( self.models[model_name]['fields'].keys() )

        return field_names

    def get_related_model_name(
        self,
        model_name: ModelName,
        field_name: str,
    ) -> str:

        # Obtención del modelo relacionado
        related_model_name = self.models[model_name]['fields'][field_name]['related_model']

        return related_model_name

    def get_related_field_name(
        self,
        model_name: ModelName,
        field_name: str,
    ) -> str:

        # Obtención del campo de ID relacionado
        related_field_name = self.models[model_name]['fields'][field_name]['related_field']

        return related_field_name

    def get_relation_model_name(
        self,
        model_name: ModelName,
        field_name: str,
    ) -> str:

        # Obtención del nombre de la tabla
        table_name = self.get_table_name(model_name)
        # Obtención del nombre del modelo relacionado
        related_model_name = self.get_related_model_name(model_name, field_name)
        # Obtención del nombre de la tabla del modelo relacionado
        related_table_name = self.get_table_name(related_model_name)
        # Se construye la llave de acceso al modelo de relación many2many
        relation_model_name = f'_rel.{table_name}.{related_table_name}'

        return relation_model_name

    def get_field_ttype(
        self,
        model_name: ModelName,
        field_name: str,
    ) -> TTypeName:

        # Obtención del tipo de dato del campo
        ttype = self.models[model_name]['fields'][field_name]['ttype']

        return ttype

    def is_computed_field(
        self,
        model_name: ModelName,
        field_name: str,
    ) -> bool:

        # Obtención del valor
        is_computed = self.models[model_name]['fields'][field_name]['is_computed']

        return is_computed

    def get_table_name(
        self,
        model_model: type[DeclarativeBase] | str,
    ) -> str:

        # Obtención del modelo en caso de haberse proporcionado una valor en texto
        if isinstance(model_model, str):
            model_model = self.get_model(model_model)
        # Obtención del nombre de la tabla
        table_name = model_model.__tablename__

        return table_name

    def get_ttype_fields(
        self,
        model_name: ModelName,
        ttype: TTypeName,
    ) -> list[str]:

        # Obtención de los campos del modelo
        model_fields = self.models[model_name]['fields']
        # Construcción de lista de campos que cumplen con el tipo de campo
        fields = [ field_name for ( field_name, atts ) in model_fields.items() if atts['ttype'] == ttype ]

        return fields

    def get_field_selection_values(
        self,
        model_name: ModelName,
        field_name: str,
    ) -> list[str]:

        # Obtención de los valores de selección desde los datos de la instancia
        selection_values = self.models[model_name]['fields'][field_name]['selection_values']

        return selection_values

    def initialize_fields_atts(
        self,
    ) -> None:

        # Registro de los atributos de campos de modelos existentes registrados
        for model_name in self.models.keys():
            self._register_table_fields_atts(model_name)

    def _register_table_fields_atts(
        self,
        model_name: ModelName,
    ) -> None:

        # Obtención de los atributos de los campos de la tabla
        fields_atts = self._m_orm.get_model_fields(model_name)

        # Registro de los campos
        for atts in fields_atts:
            # Destructuración de los valores en la tupla
            ( field_id, field_name, ttype, related_model, related_field, is_computed ) = atts
            selection_values = (
                self._main.search_read(
                    self._main._ROOT_USER,
                    'base.model.field.selection',
                    [('field_id', '=', field_id)],
                    ['name'],
                    output_format= 'dataframe',
                )
                ['name']
                .to_list()
            )
            # Registro por cada campo
            self.register_field(model_name, field_name, ttype, related_model, related_field, selection_values, is_computed)

    def _initialize(
        self,
    ) -> None:

        # Obtención del set de mapeadores de la tabla
        mappers = list(self._main._base.registry.mappers)
        # Inicialización de mapeo de modelos
        self.models = {}

        # Iteración por mapeador de SQLAlchemy
        for mapper in mappers:
            # Obtención de los datos desde los datos prestablecidos
            model_map = self._initialize_model_properties(mapper.class_, True)
            # Obtención del nombre de la tabla
            table_name: str = getattr(mapper.class_, '__tablename__')
            # Creación del nombre del modelo
            model_name = table_name.replace('_', '.')
            # Se añaden las propiedades al mapeo de módulos
            self.models[model_name] = model_map

    def _initialize_model_properties(
        self,
        table_model: type[DeclarativeBase],
        from_data: bool = False,
    ):

        # Obtención del nombre del modelo
        model_name = table_model.__tablename__.replace('_', '.')

        # Si el parámetro de obtener desde los datos predeterminados es verdedero...
        if from_data:
            # Se obtienen los datos correspondientes
            fields_data = FIELDS_ATTS[model_name]
        # Si el parámetro de obtener desde los datos predeterminados es falso...
        else:
            # Se inicializa un diccionario vacío para el mapa de campos
            fields_data = {}

        return {
            'model': table_model,
            'fields': fields_data
        }
