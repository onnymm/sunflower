from typing import TypedDict
from ..._module_types import SubtransactionCommandData

class SubTransactionsData(TypedDict):
    create: list[ SubtransactionCommandData.Create ]
    update: list[ SubtransactionCommandData.Update ]
    delete: list[ SubtransactionCommandData.Delete ]
    unlink: list[ SubtransactionCommandData.Unlink ]
    add: list[ SubtransactionCommandData.Add ]
    clean: list[ SubtransactionCommandData.Clean ]
    replace: list[ SubtransactionCommandData.Replace ]
