from ..._constants import MESSAGES
from ..._core.main import _Lylac_Core
from ..._core.modules import Access_Core
from ..._module_types import (
    ModelName,
    TransactionName,
)

class Access(Access_Core):

    def __init__(
        self,
        instance: _Lylac_Core
    ) -> None:

        # Asignación de instancia principal
        self._main = instance
        # Referencia de la instancia de autenticación
        self._auth = instance._auth

        # Se inicializa el módulo en falso
        self._active = False

    def initialize(
        self,
    ) -> None:

        # Se cambia el estado de activo a verdadero
        self._active = True

    def check_permission(
        self,
        user_id: int,
        model_name: ModelName,
        transaction: TransactionName,
    ) -> bool:

        # Si el módulo no está activo no se realiza ninguna validación
        if not self._active:
            return

        # Revisión de permiso de transacción
        granted = self._main._compiler.check_permission(user_id, model_name, transaction)

        # Si el usuario no tiene permiso de realiza la acción se arroja un error
        if not granted:
            raise PermissionError(MESSAGES.ACCESS.NOT_ALLOWED)
