from ..main import _Lylac_Core
from .._interface import Automations_Interface
from ..submods.automations import _Builder_Interface

class Automations_Core(Automations_Interface):
    _main: _Lylac_Core
    _m_builder: _Builder_Interface
