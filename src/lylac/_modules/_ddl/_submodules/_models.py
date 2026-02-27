from sqlalchemy import (
    Column,
    ForeignKey,
)
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.decl_api import DeclarativeBase
from sqlalchemy.types import (
    Boolean,
    Date,
    DateTime,
    Float,
    Integer,
    Interval,
    LargeBinary,
    String,
    Text,
    Time,
)
from ...._constants import (
    MODEL_NAME,
    ROOT_ID,
)
from ...._core.modules import DDL_Core
from ...._core.submods.ddl import _Models_Interface
from ...._data import (
    MODEL_TABLE_TEMPLATE,
    RELATION_TABLE_TEMPLATE,
)
from ...._module_types import (
    FieldDefinition,
    ModelRecordData,
    ModelTemplate as ModelTemplate, # Uso en compilación de código de archivos
    ModelName,
    TTypeName,
)
from .._module_types import ColumnGenerator

class _Models(_Models_Interface):
    _ddl: DDL_Core
    build_column: dict[TTypeName, ColumnGenerator]
    """
    ### Construcción de columna
    Este mapa de métodos construye una columna tipada para un modelo de SQLALchemy.
    Uso:
    >>> # Creación de un campo tipo 'integer'
    >>> field = NewField(...)
    >>> column = self.build_column['integer'](field)
    """

    def __init__(
        self,
        instance: DDL_Core,
    ) -> None:

        # Asignación de la instancia propietaria
        self._ddl = instance
        # Asignación de la instancia principal
        self._main = instance._main
        # Asignación de la instancia de estructura interna
        self._strc = instance._main._strc
        # Asignación de modelos base
        self._base = instance._main._base

        # Inicialización de mapa de funciones
        self._initialize()

    def create_model(
        self,
        model_name: ModelName,
    ) -> type[DeclarativeBase]:
        """
        ### Creación de modelo
        Este método crea un nuevo modelo de SQLAlchemy con sus campos base y lo
        registra en la estructura de tablas de la instancia principal.
        """
        # Creación del modelo a partir de código compilado para evitar advertencias de SQLAlchemy
        model = self._create_model_class(model_name)
        # Registro del modelo en la estructura de SQLAlchemy
        self._main._strc.register_table(model)
        # Se retorna el modelo para ser usado por otros métodos
        return model

    def create_relation(
        self,
        owner_model_name: ModelName,
        referenced_model_name: ModelName,
    ) -> type[DeclarativeBase]:

        # Creación de la tabla de relación
        model = self._create_relation_class(owner_model_name, referenced_model_name)
        # Registro de la relación en la estructura de SQLAlchemy
        self._main._strc.register_relation(model)
        # Se retorna el modelo para ser usado por otros métodos
        return model

    def delete_model(
        self,
        model_name: ModelName,
    ) -> None:
        """
        ### Eliminar modelo
        Este método elimina un modelo de SQLAlchemy del registro de Base y del mapa de tablas
        """

        # Obtención del modelo SQLAlchemy
        model_model = self._main._strc.get_model(model_name)
        # Se obtiene el esquema del registro de Base
        table_scheme = self._base.metadata.tables[model_model.__tablename__]
        # Se elimina el esquema de los modelos heredados de Base
        self._base.metadata.remove(table_scheme)
        # Se elimina el modelo de los registros del mapa de modelos
        self._main._strc.unregister_table(model_name)

    def add_field_to_model(
        self,
        model_model: type[DeclarativeBase],
        field: FieldDefinition,
    ) -> None:
        """
        ### Añadir campo al modelo
        Este método añade un nuevo campo al modelo de SQLAlchemy provisto.
        """

        # Creación de la instancia a ser añadida
        field_instance = self.build_column[field.ttype](field)
        # Se añade la instancia de campo como atributo del modelo
        setattr(
            model_model,
            field.field_name,
            field_instance,
        )
        # Se registra la instancia la modelo en el esquema de SQLAlchemy
        class_mapper(model_model).add_property(field.field_name, field_instance)

    def build_field_atts(
        self,
        params: ModelRecordData.BaseModelField,
    ) -> FieldDefinition:
        """
        ### Construcción de atributos de campo
        Construcción de atributos para usarse en nuevos campos de modelo de SQLAlchemy.
        """

        # Obtención del nombre del modelo vinculado
        model_name: ModelName = self._main.get_value(ROOT_ID, MODEL_NAME.BASE_MODEL, params['model_id'], 'model')

        # Creación de los parámetros para ser usados en las automatizaciones
        field_atts = FieldDefinition(
            field_name= params['name'],
            table_model= self._main._models.get_model_model(model_name),
            label= params['label'],
            ttype= params['ttype'],
            nullable= params['nullable'],
            is_required= params['is_required'],
            default= self._parse_default_value(params),
            unique= params['unique'],
            help_info= params['help_info'],
            related_model_id= params['related_model_id'],
            is_computed= params['is_computed'],
        )

        return field_atts

    def _create_model_class(
        self,
        model_name: ModelName,
    ) -> type[DeclarativeBase]:

        # Inicialización de un objeto
        data = {'model': None}
        # Creación del código
        f = MODEL_TABLE_TEMPLATE.format(**{'model_name': model_name})
        # Ejecución del código
        exec(f)
        # Obtención del modelo
        model_model: type[DeclarativeBase] = data['model']

        return model_model

    def _create_relation_class(
        self,
        owner_model_name: ModelName,
        referenced_model_name: ModelName,
    ) -> type[DeclarativeBase]:

        # Inicialización del objeto
        data = {'model': None}
        # Obtención de los modelos
        owner_model = self._strc.get_model(owner_model_name)
        referenced_model = self._strc.get_model(referenced_model_name)
        # Creación del código
        f = RELATION_TABLE_TEMPLATE.format(
            **{
                'main_model': owner_model.__tablename__,
                'referenced_model': referenced_model.__tablename__
            }
        )
        # Ejecución del código
        exec(f)
        # Obtención del modelo
        model_model: type[DeclarativeBase] = data['model']

        return model_model

    def _parse_default_value(
        self,
        params: ModelRecordData.BaseModelField,
    ) -> (int | float | str | bool | None):

        # Si no existe valor por defecto se termina la ejecución
        if params['default_value'] is None:
            return None

        # Obtención del tipo de dato´y valor
        ttype = params['ttype']
        value = params['default_value']

        # Si el valor es booleano
        if ttype == 'boolean':
            if value == 'true':
                return True
            else:
                return False
        # Si el valor es entero
        elif ttype == 'integer':
            return int(value)
        # Si el valor es flotante
        elif ttype == 'float':
            return float(value)
        # El valor se retorna en formato de cadena de texto
        else:
            return value

    def _build_field_kwargs(
        self,
        field: FieldDefinition
    ) -> dict:

        # Inicialización de los kwargs del campo
        field_kwargs = {}

        # Iteración por cada mapeo de atributos
        for att in self._atts:
            # Obtención del valor declarado en el objeto entrante
            field_att_value = getattr(field, att)
            # Si existe un valor declarado...
            if field_att_value is not None:
                # Se añade éste a los kwargs del campo
                field_kwargs[att] = field_att_value

        # Retorno de los kwargs del campo
        return field_kwargs

    def _get_table_name(
        self,
        model_id: int
    ) -> str:

        # Obtención del nombre de la tabla
        table_name: str = self._main.get_value(ROOT_ID, MODEL_NAME.BASE_MODEL, model_id, 'name')

        return table_name

    def _initialize(
        self
    ) -> None:

        # Inicialización de mapa de funciones
        self.build_column = {
            'integer': lambda field: Column(Integer, **self._build_field_kwargs(field)),
            'char': lambda field: Column(String(255), **self._build_field_kwargs(field)),
            'float': lambda field: Column(Float, **self._build_field_kwargs(field)),
            'boolean': lambda field: Column(Boolean, **self._build_field_kwargs(field)),
            'date': lambda field: Column(Date, **self._build_field_kwargs(field)),
            'datetime': lambda field: Column(DateTime, **self._build_field_kwargs(field)),
            'time': lambda field: Column(Time, **self._build_field_kwargs(field)),
            'duration': lambda field: Column(Interval, **self._build_field_kwargs(field)),
            'file': lambda field: Column(LargeBinary, **self._build_field_kwargs(field)),
            'text': lambda field: Column(Text, **self._build_field_kwargs(field)),
            'selection': lambda field: Column(String, **self._build_field_kwargs(field)),
            'many2one': lambda field: Column(
                Integer,
                ForeignKey(f'{self._get_table_name(field.related_model_id)}.id'),
                **self._build_field_kwargs(field)
            ),
        }


        # Inicialización de atributos de campo
        self._atts = [
            'nullable',
            'default',
            'unique',
        ]
