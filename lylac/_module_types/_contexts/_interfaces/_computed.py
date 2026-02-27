from typing import (
    Any,
    Callable,
)
from sqlalchemy import (
    Boolean,
    Integer,
    Date,
    DateTime,
    String,
    Interval,
    Time,
    func,
)
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.elements import BinaryExpression
from ...._module_types import (
    CriteriaStructure,
    AggFunctionName,
    ModelName,
    TTypeName,
)
from ...._constants import FIELD_NAME
from ..._base_categories import (
    CriteriaStructure,
    AggFunctionName,
    ModelName,
    ToCast,
)
from ._select import _SelectContextCore


class _ComputeContextCore():

    aggregation_callbacks_map: dict[AggFunctionName, Callable] = {
        'sum': func.sum,
        'count': func.count,
    }
    """
    Funciones de agregación.
    """

    FIELD_DIVISION = '.'
    """
    Símbolo de división de campos para obtención de atributos referenciados.
    """
    ID_ALIAS = f'_{FIELD_NAME.ID}'
    """
    Nombre de alias de ID.
    """

    _zero_value: dict[TTypeName, Any] = {
        'integer': 0,
        'float': 0.0,
        'duration': '00:00:00',
        'time': '00:00:00',
    }
    """
    Valor de 0 por defecto en diferentes tipos de dato.
    """

    _to_cast_ttype = {
        'boolean': Boolean,
        'char': String,
        'date': Date,
        'datetime': DateTime,
        'duration': Interval,
        'integer': Integer,
        'time': Time,
    }

    def __init__(
        self,
        model_name: ModelName,
        select_context: _SelectContextCore,
        lylac_instance,
    ) -> None:
        ...

    def __getitem__(
        self,
        field_name: str,
    ) -> InstrumentedAttribute[Any]:
        ...

    def case(
        self,
        *args: tuple[BinaryExpression, Any],
        default: Any,
    ) -> InstrumentedAttribute:
        ...

    def agg(
        self,
        composed_field_name: str,
        aggregation_function: AggFunctionName,
        search_criteria: CriteriaStructure = [],
    ) -> InstrumentedAttribute:
        ...

    def concat(
        self,
        *args,
        sep: str = '',
    ) -> InstrumentedAttribute[str]:
        ...

    def cast(
        self,
        field: InstrumentedAttribute[Any],
        ttype: ToCast,
    ) -> InstrumentedAttribute[Any]:
        ...

    def replace(
        self,
        field: InstrumentedAttribute[str],
        i: str,
        o: str,
    ) -> InstrumentedAttribute[str]:
        ...
