from typing import (
    Literal,
    Union,
)
from ._base_categories import (
    RecordIDs,
    TTypeName,
)

TTypesMapping = list[tuple[str, TTypeName]]
"""
Mapeo de nombres de campo y su respectivo tipo de dato
"""

class SubtransactionCommandData:
    Create = tuple[ dict | list[dict]]
    Update = tuple[ RecordIDs, dict]
    Delete = tuple[ RecordIDs]
    Unlink = tuple[ RecordIDs]
    Add = tuple[ RecordIDs]
    Clean = tuple
    Replace = tuple[ RecordIDs]

class SubtransactionCommandType:
    Create = Literal['create']
    Update = Literal['update']
    Delete = Literal['delete']
    Unlink = Literal['unlink']
    Add = Literal['add']
    Clean = Literal['clean']
    Replace = Literal['replace']

class SubtransactionCommand:
    Create = tuple[ SubtransactionCommandType.Create, dict | list[dict]]
    Update = tuple[ SubtransactionCommandType.Update, RecordIDs, dict]
    Delete = tuple[ SubtransactionCommandType.Delete, RecordIDs]
    Unlink = tuple[ SubtransactionCommandType.Unlink, RecordIDs]
    Add = tuple[ SubtransactionCommandType.Add, RecordIDs]
    Clean = tuple[ SubtransactionCommandType.Clean ]
    Replace = tuple[ SubtransactionCommandType.Replace, RecordIDs]

SubtransactionCommands = Union[
    SubtransactionCommand.Create,
    SubtransactionCommand.Update,
    SubtransactionCommand.Delete,
    SubtransactionCommand.Unlink,
    SubtransactionCommand.Add,
    SubtransactionCommand.Clean,
    SubtransactionCommand.Replace,
]
