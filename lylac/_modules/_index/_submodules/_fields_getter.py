from sqlalchemy.orm.attributes import InstrumentedAttribute
from ...._core.modules import Index_Core
from ...._core.submods.index import _FieldsGetter_Interface

class _FieldsGetter(_FieldsGetter_Interface):
    _index: Index_Core

    def __init__(
        self,
        instance: Index_Core,
    ) -> None:

        # Asignación de instancia propietaria
        self._index = instance
        self._models = instance._main._models

    def __getitem__(
        self,
        field_name: str,
    ) -> InstrumentedAttribute:

        # Obtención de instancia del campo solicitado
        field_instance = self._models.get_model_field(
            self._available_model,
            field_name,
        )

        return field_instance
