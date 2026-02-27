from ..main import _Lylac_Core
from .._interface import Index_Interface
from ..submods.index import _FieldsGetter_Interface

class Index_Core(Index_Interface):
    _main: _Lylac_Core
    _m_fields_getter: _FieldsGetter_Interface
