from ..main import _Lylac_Core
from .._interface import DDL_Interface
from ..submods.ddl import (
    _Database_Interface,
    _Models_Interface,
    _Reset_Interface,
)

class DDL_Core(DDL_Interface):
    _main: _Lylac_Core
    _m_db: _Database_Interface
    _m_model: _Models_Interface
    _m_reset: _Reset_Interface
