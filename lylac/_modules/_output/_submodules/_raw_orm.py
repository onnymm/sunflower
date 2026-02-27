import pandas as pd
from sqlalchemy import select, and_
from ...._module_types import (
    ModelName,
    TTypeName,
)
from ...._core.modules import Output_Core
from ...._core.submods.output import _RawORM_Interface

class _RawORM(_RawORM_Interface):
    _output: Output_Core

    def __init__(
        self,
        instance: Output_Core,
    ) -> None:

        # Asignación de la instancia propietaria
        self._ddl = instance
        # Referencia de la instancia principal
        self._main = instance._main

        # Las referencias a módulos principales no se llevan a cabo ya que este
        # módulo se inicializa primero.

    def get_fields_ttypes(
        self,
        model_name: ModelName,
        fields: list[str],
    ) -> dict[str, TTypeName]:

        # Obtención de la ID del modelo
        model_id = self._get_model_id(model_name)

        # Creación del query
        stmt = (
            select(self._main._index['base.model.field']['name'], self._main._index['base.model.field']['ttype'])
            .where(
                and_(
                    self._main._index['base.model.field']['model_id'] == model_id,
                    self._main._index['base.model.field']['name'].in_(fields)
                )
            )
        )

        # Ejecución del query
        response = self._main._connection.execute(stmt)

        # Obtención de los datos
        data = pd.DataFrame(response.fetchall()).to_dict('records')

        return {field['name']: field['ttype'] for field in data}

    def _get_model_id(
        self,
        model_name: ModelName
    ) -> None:

        # Creación del query
        stmt = (
            select(self._main._index['base.model']['id'])
            .where(self._main._index['base.model']['model'] == model_name)
        )

        # Ejecución del query
        response = self._main._connection.execute(stmt)

        # Obtención de la ID de modelo
        model_id = int(
            pd.DataFrame(
                response
                .fetchall()
            )
            .at[0, 'id']
        )

        return model_id
