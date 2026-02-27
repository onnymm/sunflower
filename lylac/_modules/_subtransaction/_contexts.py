from typing import (
    Generic,
)
from ..._module_types import (
    _M,
    ModelName,
    RecordIDs,
    SubtransactionCommands,
    SubtransactionMode,
)
from ._module_types import SubTransactionsData

class _BaseRelactionalContext():
    subtransaction_commands: list[SubtransactionCommands]
    """
    ### Comandos de subtransacción
    Lista de comandos de subtransacción.
    """
    subtransactions_data: SubTransactionsData
    """
    ### Datos de subtransacciones
    Datos de subtransacciones a ser realizadas.
    """
    transaction_mode: _M
    """
    ### Modo de transacciones
    Modo de transacciones del contexto. Puede ser creación o modificación.
    """
    model_name: ModelName
    """
    Nombre del modelo.
    """
    related_model_name: ModelName
    """
    Nombre del modelo relacionado.
    """
    field_name: str
    """
    Nombre del campo.
    """
    parent_record_ids: RecordIDs | None
    """
    IDs del registro padre. En caso de ser modo de creación el valor es `None`.
    """
    index: int | None
    """
    Índice de transacción. En caso de ser modo de modificación el valor es `None`.
    """

class RelationalContext(_BaseRelactionalContext, Generic[_M]):

    def __init__(
        self,
        model_name: ModelName,
        related_model_name: ModelName,
        many2many_field_name: str,
        parent_record_ids: RecordIDs | None,
        subtransaction_commands: list[SubtransactionCommands],
        transaction_mode: SubtransactionMode,
        index: int | None = None
    ) -> None:

        # Se guardan los valores en la instancia
        self.model_name = model_name
        self.related_model_name = related_model_name
        self.field_name = many2many_field_name
        self.parent_record_ids = parent_record_ids
        self.subtransaction_commands = subtransaction_commands
        self.transaction_mode = transaction_mode
        self.index = index
        self.subtransactions_per_field = []

        self.subtransactions_data: SubTransactionsData = {
            'create': [],
            'update': [],
            'delete': [],
            'add': [],
            'unlink': [],
            'clean': [],
            'replace': [],
        }
