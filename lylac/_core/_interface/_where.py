from typing import overload
from sqlalchemy import (
    Select,
    Update,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.elements import BinaryExpression
from ..._module_types import (
    _T,
    CriteriaStructure,
)

class Where_Interface():

    @overload
    def add_query(
        self,
        stmt: Select[_T],
        model_model: type[DeclarativeBase],
        search_criteria: CriteriaStructure,
    ) -> Select[_T]:
        ...

    @overload
    def add_query(
        self,
        stmt: Update[_T],
        model_model: type[DeclarativeBase],
        search_criteria: CriteriaStructure,
    ) -> Update[_T]:
        ...

    def build_where(
        self,
        model_model: type[DeclarativeBase],
        search_criteria: CriteriaStructure,
    ) -> BinaryExpression:
        ...
