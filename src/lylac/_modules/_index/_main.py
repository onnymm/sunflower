from sqlalchemy.orm.decl_api import DeclarativeBase
from ..._core.modules import Index_Core
from ..._core.main import _Lylac_Core
from ..._module_types import ModelName
from ._submodules import _FieldsGetter

class Index(Index_Core):

    def __init__(
        self,
        instance: _Lylac_Core,
    ) -> None:

        # Asignación de instancia principal
        self._main = instance
        # Asignación de objeto de obtención de campos
        self._m_fields_getter = _FieldsGetter(self)

        # Referencia del módulo de modelos
        self._models = instance._models

    def __getitem__(
        self,
        model: ModelName | type[DeclarativeBase],
    ) -> _FieldsGetter:

        # Obtención de modelo de SQLAlchemy si es que fue provisto solo el nombre
        if isinstance(model, str):
            model_model = self._main._models.get_model_model(model)
        # Reasignación de variable en caso de que haya sido provisto el modelo
        else:
            model_model = model

        # Se muestra el modelo en el selector de campo
        self._m_fields_getter._available_model = model_model

        # Se retorna el selector de campo
        return self._m_fields_getter
