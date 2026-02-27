from ...._core.modules import Subtransaction_Core
from .._contexts import RelationalContext
from typing import (
    Callable,
    overload,
)
from ...._module_types import (
    SubtransactionCreateMode,
    SubtransactionUpdateMode,
    Many2ManyUpdatesOnCreateCallback,
    Many2ManyUpdatesOnUpdateCallback,
    RecordIDs,
)

class _Wrapping():

    def __init__(
        self,
        instance: Subtransaction_Core,
    ) -> None:

        # Asignación de la instancia propietaria
        self._subtransaction = instance
        # Asignación de la instancia principal
        self._main = instance._main

        # Asignación de la instancia de estructura interna
        self._strc = instance._main._strc
        # Asignación de la instancia de compilador
        self._compiler = instance._main._compiler

    @overload
    def create_postcallback(
        self,
        callback: Callable[[list], None],
        ctx: RelationalContext[SubtransactionCreateMode],
    ) -> Many2ManyUpdatesOnCreateCallback:
        ...

    @overload
    def create_postcallback(
        self,
        callback: Callable[[list], None],
        ctx: RelationalContext[SubtransactionUpdateMode],
    ) -> Many2ManyUpdatesOnUpdateCallback:
        ...

    def create_postcallback(
        self,
        subtransactions_per_type: Callable[[list], None],
        ctx: RelationalContext,
    ) -> Many2ManyUpdatesOnUpdateCallback | Many2ManyUpdatesOnCreateCallback:
        """
        ### Creación de actualizaciones de tipos `many2many`
        Este método permite crear una función que permite realizar actualizaciones
        de datos en registros referenciados tras la ejecución principal de una
        transacción de creación o modificación de registros.

        Las funciones para cada tipo de transacción son distintas:

        #### Creación
        En método de transacción, una función se crea por cada ID de registro
        creado. La función creada mantiene el contexto del orden de las IDs por el
        tamaño de la lista de datos provista en la función principal de Lylac.
        
        La función recibe la lista de IDs completa pero solo procesa la ID a la que
        corresponde gracias a que se mantiene el índice de registro al que se
        asigna ésta.

        >>> def updates_on_create(created_ids: list[int]):
        >>>     ...

        #### Actualización
        En método de actualización, se crea una función para toda la transacción,
        que mantiene contexto de las IDs que han sido modificadas por el método
        principal de Lylac. La función no recibe ningún argumento y realiza las
        actualizaciones de valores referenciados que son un solo diccionario.

        >>> def updates_on_update():
        >>>     ...
        """

        # Si el modo de transacción es creación...
        if ctx.transaction_mode == 'create':
            # Se inicializa función que recibe lista de IDs de registros creados
            def wrapped_subtransactions_per_type(created_ids: RecordIDs):
                # Se extrae la ID del índice almacenado en el contexto
                created_id = [ created_ids[ctx.index] ]
                # Ejecución de la función con la ID correspondiente.
                subtransactions_per_type(created_id)

        # Si el modo de transacción es actualización...
        else:
            # Se inicializa función que no recibe ningún argumento
            def wrapped_subtransactions_per_type():
                # Se ejecuta función con los datos provistos a este método
                subtransactions_per_type(ctx.parent_record_ids)

        return wrapped_subtransactions_per_type
