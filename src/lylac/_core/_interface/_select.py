from typing import Any
from ..._module_types import (
    TTypesMapping,
    ModelName,
)
from sqlalchemy.sql.selectable import Select

class Select_Interface():

    def build(
        self,
        model_name: ModelName,
        fields: list[str] = [],
    ) -> tuple[Select[Any], TTypesMapping]:
        ...
