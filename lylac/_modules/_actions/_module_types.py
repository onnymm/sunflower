from ..._contexts._actions import ActionCallback
from ..._module_types import ModelName

_ModelActions = dict[str, ActionCallback]
"""
#### Acciones de modelo
Diccionario que agrupa las acciones de un modelo.
"""
ActionsHub = dict[ModelName, _ModelActions]
"""
#### Núcleo de acciones
Diccionario que reúne las acciones de todos los modelos de la base de datos.
"""
