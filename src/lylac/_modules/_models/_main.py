from typing import Any
from sqlalchemy import (
    Subquery,
    inspect,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.properties import ColumnProperty
from ..._constants import FIELD_NAME
from ..._core.modules import Models_Core
from ..._core.main import _Lylac_Core
from ..._module_types import ModelName

class Models(Models_Core):

    def __init__(
        self,
        instance: _Lylac_Core,
    ) -> None:

        # Asignación de la instancia propietaria
        self._main = instance

        # Referencia al módulo de estructura interna
        self._strc = instance._strc

    def get_model_name(
        self,
        model_model: type[DeclarativeBase],
    ) -> ModelName:

        # Obtención del nombre del modelo
        model_name: ModelName = model_model.__tablename__.replace('_', '.')

        return model_name

    def get_model_model(
        self,
        model_name: ModelName,
    ) -> type[DeclarativeBase]:

        # Obtención de la referencia mapeada
        return self._strc.get_model(model_name)

    def get_id_field(
        self,
        model_model: type[DeclarativeBase]
    ) -> InstrumentedAttribute[int]:

        # Retorno de la instancia del campo de ID
        return getattr(model_model, FIELD_NAME.ID)

    def get_model_field(
        self,
        model_model: type[DeclarativeBase] | Subquery,
        field: str,
    ) -> InstrumentedAttribute:

        if isinstance(model_model, Subquery):
            target = model_model.c
        else:
            target = model_model

        # Obtención del campo, atributo de la instancia de la tabla
        return getattr(target, field)

    def get_model_fields(
        self,
        model_model: type[DeclarativeBase],
        fields: list[str] = [],
        include_id: bool = True,
    ) -> list[InstrumentedAttribute[Any]]:

        # Inicialización de la lista con el valor de 'id' como primer elemento
        id_field = [FIELD_NAME.ID,]

        # Obtención de todos los campos
        if len(fields) == 0:
            # Obtención de columnas con relación para evitar productos cartesianos
            instance_relationships = { _relationship.key for _relationship in inspect(model_model).relationships }
            mapper = inspect(model_model)
            all_columns = [column.key for column in mapper.attrs if isinstance(column, ColumnProperty)]
            instance_fields = [col for col in all_columns if col not in instance_relationships]

            # Asignación de valor a la variable entrante
            fields = instance_fields

        if include_id:
            # Remoción del campo de 'ID en caso de ser solicitado, para evitar campos duplicados en el retorno de la información
            try:
                fields.remove(FIELD_NAME.ID)
            except ValueError:
                pass

            # Suma del campo 'ID' como primer elemento de los campos a retornar
            table_fields = id_field + fields

        # Inclusión del ID solo de forma explícita
        else:
            table_fields = fields

        # Obtención de los atributos de la tabla a partir de los nombres de los campos y retorno en una lista para ser usados en el query correspondiente
        return [ getattr(model_model, field) for field in table_fields ]
