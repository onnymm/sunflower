from typing import Optional
from sqlalchemy import Select
from sqlalchemy.orm.decl_api import DeclarativeBase
from ..._module_types import (
    _T,
    ItemOrList,
)

class Query_Interface():

    def build_sort(
        self,
        stmt: Select[_T],
        model_model: type[DeclarativeBase],
        sortby: ItemOrList[str],
        ascending: ItemOrList[bool],
    ) -> Select[_T]:
        ...

    def build_segmentation(
        self,
        stmt: Select[_T],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Select[_T]:
        ...
