from typing import Tuple
from ...._module_types import TTypeName

class _RawORM_Interface():

    def get_model_fields(
        self,
        model_name,
    ) -> list[Tuple[int, str, TTypeName, None | str, None | str, bool]]:
        ...
