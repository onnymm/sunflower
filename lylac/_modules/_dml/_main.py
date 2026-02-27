from sqlalchemy import update, delete
from sqlalchemy.orm import Session
from ..._constants import FIELD_NAME
from ..._core.main import _Lylac_Core
from ..._core.modules import DML_Core
from ..._module_types import (
    CriteriaStructure,
    ModelTemplate,
    RecordData,
    ItemOrList,
    ModelName,
)

class DMLManager(DML_Core):

    def __init__(
        self,
        instance: _Lylac_Core,
    ) -> None:

        # Asignación de la instancia propietaria
        self._main = instance
        # Asignación de la instancia de conexión
        self._connection = instance._connection
        # Asignación de la instancia de índice
        self._index = instance._index
        # Asignación de la instancia de gestión de modelos de SQLAlchemy
        self._models = instance._models
        # Asignación de la instancia de estructura interna
        self._strc = instance._strc
        # Asignación del módulo de query WHERE
        self._where = instance._where
        # Asignación del motor de conexión
        self._engine = instance._engine

    def create(
        self,
        model_name: ModelName,
        data: list[RecordData],
    ) -> list[int]:

        # Se remueven los campos many2many
        self._remove_many2many_fields(model_name, data)
        # Obtención de la instancia de la tabla
        model_model = self._strc.get_model(model_name)
        # Instanciación de objetos para crear en la base de datos
        records: list[ModelTemplate] = [ model_model(**record) for record in data ]

        # Ejecución de la transacción
        with Session(self._engine) as session:
            session.add_all(records)
            session.commit()

            # Actualización de los objetos registrados
            for record in records:
                session.refresh(record)

        # Obtención de las IDs creadas
        inserted_records = [ record.id for record in records ]

        return inserted_records

    def update_where(
        self,
        model_name: ModelName,
        search_criteria: CriteriaStructure,
        data: RecordData,
    ) -> bool:

        # Obtención de la instancia de la tabla
        model_model = self._models.get_model_model(model_name)
        # Creación del query base
        stmt = update(model_model)
        # Creación del segmento WHERE
        stmt = self._where.add_query(stmt, model_model, search_criteria)
        # Declaración de valores a cambiar
        stmt = stmt.values(data)
        # Declaración para obtener las IDs modificadas
        stmt = stmt.returning(self._models.get_id_field(model_model))

        # Ejecución de la transacción
        response = self._connection.execute(stmt, commit= True)
        # Obtención de las IDs creadas
        updated_records: list[int] = [ getattr(row, 'id') for row in response ]

        return updated_records

    def delete(
        self,
        model_name: ModelName,
        record_ids: ItemOrList[int]
    ) -> bool:

        # Obtención de la instancia de la tabla
        model_model = self._models.get_model_model(model_name)
        # Obtención de la columna de ID de la tabla
        c_model_model__id = self._index[model_model][FIELD_NAME.ID]
        # Creación de la condición de búsqueda
        condition = c_model_model__id.in_(record_ids)
        # Creación del query
        stmt = (
            delete(model_model)
            .where(condition)
            .returning(c_model_model__id)
        )
        # Ejecución de la transacción
        response = self._connection.execute(stmt, commit= True)
        # Obtención de las IDs encontradas
        deleted_ids: list[int] = [ getattr(row, FIELD_NAME.ID) for row in response ]

        return deleted_ids

    def _remove_many2many_fields(
        self,
        model_name: ModelName,
        data: list[RecordData],
    ) -> None:

        # Obtención de los nombres de campos many2many del modelo
        many2many_fields = self._strc.get_ttype_fields(model_name, 'many2many')

        # Iteración por cada registro a crear
        for record in data:
            # Búsqueda por cada campo many2many que pueda existir en el diccionario
            for many2many_field in many2many_fields:
                # Si se encuentra un campo many2many...
                if many2many_field in record.keys():
                    # Se remueve éste de los datos
                    del record[many2many_field]
