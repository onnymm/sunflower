from sqlalchemy import text
from ...._constants import ROOT_ID
from ...._core.modules import DDL_Core
from ...._core.submods.ddl import _Database_Interface
from ...._module_types import (
    FieldDefinition,
    TTypeName,
)

class _Database(_Database_Interface):
    """
    ### Métodos de base de datos
    Este submódulo agrupa todos los métodos relacionados con la manipulación de la
    base de datos.
    """
    _ddl: DDL_Core
    # Mapeo de nombres a tipos de dato en SQL
    _name_to_type: dict[TTypeName, str] = {
        'integer': 'INTEGER',
        'char': 'VARCHAR(255)',
        'float': 'FLOAT',
        'boolean': 'BOOLEAN',
        'date': 'DATE',
        'datetime': 'TIMESTAMP',
        'time': 'TIME',
        'duration': 'INTERVAL',
        'file': 'BYTEA',
        'text': 'TEXT',
        'selection': 'VARCHAR(100)',
        'many2one': 'INTEGER',
    }

    def __init__(
        self,
        instance: DDL_Core,
    ) -> None:

        # Asignación de la instancia propietaria
        self._ddl = instance
        # Referencia del módulo principal
        self._main = instance._main
        # Referencia del módulo de conexión
        self._connection = instance._main._connection

    def add_column(
        self,
        params: FieldDefinition,
    ):
        """
        ### Añadir columna a tabla
        Este método añade una columna a la tabla especificada con los atributos
        especificados en la declaración del objeto entrante.
        """

        # Creación de la sentencia
        stmt = text(
            f"""
            {self._query_add_column(params)}
            {self._query_default_value(params)}
            {self._query_foreign_key(params)}
            """
        )
        # Ejecución de la transacción
        self._connection.execute(stmt, commit= True)

    def drop_column(
        self,
        table_name: str,
        column_name: str,
    ) -> None:

        # Creación del query a ejecutar
        stmt = text(f'ALTER TABLE {table_name} DROP COLUMN {column_name};')
        # Ejecución de la transacción en la base de datos
        self._connection.execute(stmt, commit= True)

    def _query_add_column(
        self,
        params: FieldDefinition,
    ) -> str:

        # Obtención de los atributos
        table_name = params.table_model.__tablename__
        column_name = params.field_name
        column_type = self._name_to_type[params.ttype]

        # Construcción del framento "add column"
        query = f'ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}'

        return query

    def _query_default_value(
        self,
        params: FieldDefinition,
    ) -> str:

        # Si no existe un valor por defecto
        if params.default is None:
            return ';'

        # Si el valor es de tipo cadena de texto...
        if isinstance(params.default, str):
            value = f"'{params.default}'"
        # Si el valor es de tipo booleano...
        elif isinstance(params.default, bool):
            value = str(params.default).upper()
        # Si el valor es de otro tipo de dato...
        else:
            value = str(params.default)

        # Retorno del framgento "default value"
        return f' DEFAULT {value};'

    def _query_foreign_key(
        self,
        params: FieldDefinition,
    ) -> str:

        if params.ttype != 'many2one':
            return ''

        # Obtención de los atributos
        table_name = params.table_model.__tablename__
        column_name = params.field_name
        constraint_name = f'{table_name}_{column_name}_fkey'
        referenced_table_name = self._ddl._main.get_value(ROOT_ID, 'base.model', params.related_model_id, 'name')

        # Construcción del query
        query = (
            f"""
            ALTER TABLE {table_name}
            ADD CONSTRAINT {constraint_name}
            FOREIGN KEY ({column_name})
            REFERENCES {referenced_table_name}(id)
            ON DELETE SET NULL;
            """
        )

        return query
