from ..main import _Lylac_Core
from .._interface import Connection_Interface
from ..submods.connection import _Env_Interface

class Connection_Core(Connection_Interface):
    _main: _Lylac_Core
    _m_env: _Env_Interface
