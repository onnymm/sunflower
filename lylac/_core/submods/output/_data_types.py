import pandas as pd
from typing import Callable
from ...._module_types import TTypeName

class _DataTypes_Interface():
    recover_ttype: dict[TTypeName, Callable[[pd.DataFrame, str], pd.DataFrame]]
