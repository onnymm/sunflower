from typing import Tuple
import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import aliased
from ...._constants import (
    FIELD_NAME,
    MODEL_NAME,
)
from ...._core.modules import Structure_Core
from ...._core.submods.structure import _RawORM_Interface
from ...._module_types import TTypeName

class _RawORM(_RawORM_Interface):
    _strc: Structure_Core

    def __init__(
        self,
        instance: Structure_Core,
    ) -> None:

        # Asignación de instancia propietaria
        self._strc = instance
        # Asignación de instancia
        self._main = instance._main

    def get_model_fields(
        self,
        model_name,
    ) -> list[Tuple[int, str, TTypeName, None | str, None | str]]:

        # Obtención de modelos base
        BaseModel = self._main._models.get_model_model(MODEL_NAME.BASE_MODEL)
        BaseModelField = self._main._models.get_model_model(MODEL_NAME.BASE_MODEL_FIELD)

        # Creación de alias de modelos
        FieldModel = aliased(BaseModel)
        RelatedModel = aliased(BaseModel)

        # Creación del query
        stmt = (
            select(
                self._main._index[BaseModelField][FIELD_NAME.ID],
                self._main._index[BaseModelField]['name'],
                self._main._index[BaseModelField]['ttype'],
                self._main._index[RelatedModel]['model'],
                self._main._index[BaseModelField]['related_field'],
                self._main._index[BaseModelField]['is_computed'],
            )
            .outerjoin(
                FieldModel,
                self._main._index[BaseModelField]['model_id'] == self._main._index[FieldModel][FIELD_NAME.ID],
            )
            .outerjoin(
                RelatedModel,
                self._main._index[BaseModelField]['related_model_id'] == self._main._index[RelatedModel][FIELD_NAME.ID],
            )
            .where(
                self._main._index[FieldModel]['model'] == model_name
            )
        )

        # Ejecución del query
        response = self._main._connection.execute(stmt)

        return (
            [
                tuple(item) for item in (
                    pd.DataFrame(
                        response
                        .fetchall()
                    )
                    .T
                    .to_dict('list')
                    .values()
                )
            ]
        )
