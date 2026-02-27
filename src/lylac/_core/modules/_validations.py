from ..main import _Lylac_Core
from .._interface import Validations_Interface
from ..submods.validations import _Initialize_Interface

class Validations_Core(Validations_Interface):
    _main: _Lylac_Core
    _m_initialize: _Initialize_Interface
