from ..main import _Lylac_Core
from .._interface import Structure_Interface
from ..submods.structure import _RawORM_Interface

class Structure_Core(Structure_Interface):
    _main: _Lylac_Core
    _m_orm: _RawORM_Interface
