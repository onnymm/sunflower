from typing import (
    Callable,
    overload,
)
from ..._module_types import (
    _C,
    _E,
    _T,
)

class Algorythms_Interface():

    @overload
    def find_duplicates(
        self,
        data: list[_T],
        extractor: Callable[[_T], _E] = lambda value: value,
        groupby: None = None,
    ) -> list[_E]:
        ...

    @overload
    def find_duplicates(
        self,
        data: list[_T],
        extractor: Callable[[_T], _E],
        groupby: Callable[[_T], _C],
    ) -> dict[_C, list[_E]]:
        ...

    def get_from(
        self,
        data: list[_T],
        condition: Callable[[_T], bool],
        value: Callable[[_T], _E] = lambda value: value,
    ) -> list[_E]:
        ...
