from ...._module_types import (
    ModelName,
    TTypeName,
)

class _RawORM_Interface():

    def get_fields_ttypes(
        self,
        model_name: ModelName,
        fields: list[str],
    ) -> dict[str, TTypeName]:
        ...
