from ..._module_types import (
    ModelName,
    TTypeName,
)
from ..._module_types._contexts import ComputedFieldCallback

class Compute_Interface():

    hub: dict[ModelName, dict[str, ComputedFieldCallback]]

    def _initialize(
        self,
    ) -> None:
        ...

    def initialize_default_computed_fields(
        self,
    ) -> None:
        ...

    def register_computed_field(
        self,
        model_name: ModelName,
        ttype: TTypeName,
        field_name: str,
        field_label: str,
        compute_field_callback: ComputedFieldCallback,
    ) -> None:
        ...

    def register_model(
        self,
        model_name: ModelName,
    ) -> None:
        ...
