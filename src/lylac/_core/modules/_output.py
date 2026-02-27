from ..main import _Lylac_Core
from .._interface import Output_Interface
from ..submods.output import (
    _DataTypes_Interface,
    _RawORM_Interface,
)

class Output_Core(Output_Interface):
    _main: _Lylac_Core
    _m_data: _DataTypes_Interface
    _m_orm: _RawORM_Interface
