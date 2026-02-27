from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.sql.selectable import (
    Select,
    TypedReturnsRows,
)
from ..._module_types import _T

class Connection_Interface():

    def execute(
        self,
        statement: Select[_T] | TypedReturnsRows[_T],
        commit: bool = False
    ) -> CursorResult[_T]:
        ...
