from ..._constants import MESSAGES
from ..._module_types import (
    ModelName,
    TransactionName,
)

class Access_Interface():

    def initialize(
        self,
    ) -> None:
        ...

    def check_permission(
        self,
        user_id: int,
        model_name: ModelName,
        transaction: TransactionName,
    ) -> bool:
        ...
