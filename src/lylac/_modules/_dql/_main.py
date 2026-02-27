from typing import Optional
import pandas as pd
from sqlalchemy import (
    select,
    func,
)
from ..._constants import FIELD_NAME
from ..._core.main import _Lylac_Core
from ..._core.modules import DQL_Core
from ..._module_types import (
    CriteriaStructure,
    ItemOrList,
    ModelName,
    OutputOptions,
    RecordValue,
)

class DQLManager(DQL_Core):

    def __init__(
        self,
        instance: _Lylac_Core,
    ) -> None:

        # Asignación del módulo principal
        self._main = instance
        # Asignación de la instancia de conexión
        self._connection = instance._connection
        # Asignación de la instancia de manejo de modelos de SQLAlchemy
        self._models = instance._models
        # Asignación de la instancia de manejo de formato de salida
        self._output = instance._output
        # Asignación de la instancia query
        self._query = instance._query
        # Asignación de la instancia de SELECT
        self._select = instance._select
        # Asignación de la instancia de estructura interna
        self._strc = instance._strc
        # Asígnación de la instancia WHERE
        self._where = instance._where

    def search(
        self,
        model_name: ModelName,
        search_criteria: CriteriaStructure,
        offset: Optional[int],
        limit: Optional[int],
    ) -> list[int]:

        # Creación del query SELECT
        ( stmt, _ ) = self._select.build(model_name, [FIELD_NAME.ID])
        # Obtención de la instancia de la tabla
        model_model = self._strc.get_model(model_name)
        # Creación del segmento WHERE en caso de haberlo
        stmt = self._where.add_query(stmt, model_model, search_criteria)
        # Ordenamiento de los datos
        stmt = self._query.build_sort(stmt, model_model, FIELD_NAME.ID, True)
        # Segmentación de inicio y fin en caso de haberlos
        stmt = self._query.build_segmentation(stmt, offset, limit)
        # Ejecución de la transacción
        response = self._connection.execute(stmt)
        # Obtención de las IDs encontradas
        found_ids = self._output.get_found_ids(response)

        return found_ids

    def read(
        self,
        model_name: ModelName,
        record_ids: ItemOrList[int],
        fields: list[str],
        sortby: ItemOrList[str],
        ascending: ItemOrList[bool],
        output_format: Optional[OutputOptions],
        only_ids_in_relations: bool,
    ) -> pd.DataFrame | list[dict[str, RecordValue]]:

        # Obtención de la instancia de la tabla
        model_model = self._models.get_model_model(model_name)
        # Creación del query base
        ( stmt, ttypes ) = self._select.build(model_name, fields)
        # Creación del segmento WHERE
        stmt = self._where.add_query(stmt, model_model, [(FIELD_NAME.ID, 'in', record_ids)])
        # Creación de parámetros de ordenamiento
        stmt = self._query.build_sort(
            stmt,
            model_model,
            sortby,
            ascending,
        )
        # Ejecución de la transacción
        response = self._connection.execute(stmt)
        # Inicialización del DataFrame de retorno
        data = pd.DataFrame( response.fetchall() )
        # Procesamiento de salida de datos
        processed_data = self._output.build_output(
            data,
            ttypes,
            output_format,
            'dataframe',
            only_ids_in_relations
        )

        return processed_data

    def search_read(
        self,
        model_name: ModelName,
        search_criteria: CriteriaStructure = [],
        fields: list[str] = [],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sortby: Optional[ ItemOrList[str] ] = None,
        ascending: ItemOrList[bool] = True,
        output_format: Optional[OutputOptions] = None,
        only_ids_in_relations: bool = False,
    ) -> pd.DataFrame | dict[str, RecordValue]:

        # Obtención de la instancia de la tabla
        model_model = self._models.get_model_model(model_name)
        # Creación del query base
        ( stmt, ttypes ) = self._select.build(model_name, fields)
        # Creación del segmento WHERE en caso de haberlo
        stmt = self._where.add_query(stmt, model_model, search_criteria)
        # Creación de parámetros de ordenamiento
        stmt = self._query.build_sort(
            stmt,
            model_model,
            sortby,
            ascending,
        )
        # Segmentación de inicio y fin en caso de haberlos
        stmt = self._query.build_segmentation(stmt, offset, limit)

        # Ejecución de la transacción
        response = self._connection.execute(stmt)
        # Inicialización del DataFrame de retorno
        data = pd.DataFrame( response.fetchall() )
        # Procesamiento de salida de datos
        processed_data = self._output.build_output(
            data,
            ttypes,
            output_format,
            'dataframe',
            only_ids_in_relations
        )

        return processed_data

    def search_count(
        self,
        model_name: ModelName,
        search_criteria: CriteriaStructure,
    ) -> int:

        # Obtenciónde la instancia de la tabla
        model_model = self._models.get_model_model(model_name)
        # Creación del query base
        stmt = (
            select( func.count() )
            .select_from(model_model)
        )
        # Creación del segmento WHERE en caso de haberlo
        stmt = self._where.add_query(stmt, model_model, search_criteria)
        # Ejecución de la transacción
        response = self._connection.execute(stmt)
        # Obtención del conteo de registro
        count = response.scalar()

        return count
