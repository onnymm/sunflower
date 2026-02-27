from ..main import _Lylac_Core
from .._interface import Auth_Interface
from ..submods.auth import (
    _Session_Interface,
    _Token_Interface,
)

class Auth_Core(Auth_Interface):
    _main: _Lylac_Core
    _m_session: _Session_Interface
    _m_token: _Token_Interface
