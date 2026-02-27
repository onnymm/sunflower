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
    ModelName,
    RecordIDs,
    SubtransactionCommands,
    SubtransactionName,
)
from ._wrapping import _Wrapping

class _One2Many():

    @overload
    def _create_records(
        ctx: RelationalContext[SubtransactionCreateMode],
    ) -> Many2ManyUpdatesOnCreateCallback:
        ...

    @overload
    def _create_records(
        ctx: RelationalContext[SubtransactionUpdateMode],
    ) -> Many2ManyUpdatesOnUpdateCallback:
        ...

    @overload
    def _update_records(
        self,
        ctx: RelationalContext[SubtransactionCreateMode],
    ) -> Many2ManyUpdatesOnCreateCallback:
        ...

    @overload
    def _update_records(
        self,
        ctx: RelationalContext[SubtransactionUpdateMode],
    ) -> Many2ManyUpdatesOnUpdateCallback:
        ...

    @overload
    def _delete_records(
        self,
        ctx: RelationalContext[SubtransactionCreateMode],
    ) -> Many2ManyUpdatesOnCreateCallback:
        ...

    @overload
    def _delete_records(
        self,
        ctx: RelationalContext[SubtransactionUpdateMode],
    ) -> Many2ManyUpdatesOnUpdateCallback:
        ...

    @overload
    def _add_records(
        self,
        ctx: RelationalContext[SubtransactionCreateMode],
    ) -> Many2ManyUpdatesOnCreateCallback:
        ...

    @overload
    def _add_records(
        self,
        ctx: RelationalContext[SubtransactionUpdateMode],
    ) -> Many2ManyUpdatesOnUpdateCallback:
        ...

    @overload
    def _unlink_records(
        self,
        ctx: RelationalContext[SubtransactionCreateMode],
    ) -> Many2ManyUpdatesOnCreateCallback:
        ...

    @overload
    def _unlink_records(
        self,
        ctx: RelationalContext[SubtransactionUpdateMode],
    ) -> Many2ManyUpdatesOnUpdateCallback:
        ...

    @overload
    def _clean_records(
        self,
        ctx: RelationalContext[SubtransactionCreateMode],
    ) -> Many2ManyUpdatesOnCreateCallback:
        ...

    @overload
    def _clean_records(
        self,
        ctx: RelationalContext[SubtransactionUpdateMode],
    ) -> Many2ManyUpdatesOnUpdateCallback:
        ...

    @overload
    def _replace_records(
        self,
        ctx: RelationalContext[SubtransactionCreateMode],
    ) -> Many2ManyUpdatesOnCreateCallback:
        ...

    @overload
    def _replace_records(
        self,
        ctx: RelationalContext[SubtransactionUpdateMode],
    ) -> Many2ManyUpdatesOnUpdateCallback:
        ...

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

        # TODO El submódulo debe utilizarse desde el módulo propietario pero se requiere llevar el tipado del contexto
        # Uso de submódulo
        self._m_wrapping = _Wrapping(instance)

        # Inicialización de mapa de subtransacciones
        self._initialize_subtransactions_map()

    def create_one2many_updates_for_creation_mode(
        self,
        model_name: ModelName,
        one2many_field: str,
        subtransaction_commands: list[SubtransactionCommands],
        index: int,
    ) -> list[Many2ManyUpdatesOnCreateCallback]:

        # Obtención del modelo relacionado
        related_model_name = self._strc.get_related_model_name(model_name, one2many_field)
        # Se crea la instancia del contexto
        ctx = RelationalContext[SubtransactionCreateMode](
            model_name,
            related_model_name,
            one2many_field,
            None,
            subtransaction_commands,
            'create',
            index,
        )

        # Creación de las funciones de subtransacciones por campo
        subtransactions_per_field = self._create_subtransactions_per_field(ctx)

        return subtransactions_per_field

    def create_one2many_updates_for_update_mode(
        self,
        model_name: ModelName,
        one2many_field: str,
        subtransaction_commands: list[SubtransactionCommands],
        record_ids: RecordIDs,
    ) -> list[Many2ManyUpdatesOnUpdateCallback]:

        # Obtención del modelo relacionado
        related_model_name = self._strc.get_related_model_name(model_name, one2many_field)
        # Se crea la instancia del contexto
        ctx = RelationalContext[SubtransactionUpdateMode](
            model_name,
            related_model_name,
            one2many_field,
            record_ids,
            subtransaction_commands,
            'update',
        )

        # Creación de las funciones de subtransacciones por campo
        subtransactions_per_field = self._create_subtransactions_per_field(ctx)

        return subtransactions_per_field

    def _create_subtransactions_per_field(
        self,
        ctx: RelationalContext,
    ) -> list[Many2ManyUpdatesOnCreateCallback] | list[Many2ManyUpdatesOnUpdateCallback]:

        # Inicialización de lista de transacciones por campo
        subtransactions_per_field: list[Many2ManyUpdatesOnCreateCallback] | list[Many2ManyUpdatesOnUpdateCallback] = []

        # Iteración por cada valor para asignar a la ejecución
        for subtransaction_command in ctx.subtransaction_commands:
            # Obtención del tipo de subtransacción
            subtransaction_type: SubtransactionName = subtransaction_command[0]
            # Obtención de los datos a usar
            subtransaction_data = subtransaction_command[1:]
            # Se asignan los datos
            ctx.subtransactions_data[subtransaction_type].append(subtransaction_data)

        # Iteración por cada tipo de transacción
        for subtransaction_name in ctx.subtransactions_data.keys():
            # Si existen datos en el tipo de transacción...
            if ctx.subtransactions_data[subtransaction_name]:
                # Obtención de la función que generará las subtransacciones por tipo
                callback = self._subtransactions_map[subtransaction_name]
                # Creación de función de subtransacciones por tipo
                subtransactions_per_type: Many2ManyUpdatesOnCreateCallback | Many2ManyUpdatesOnUpdateCallback = callback(ctx)
                # Se añade la función de subtransacciones por tipo a la lista de transacciones por campo
                subtransactions_per_field.append(subtransactions_per_type)

        return subtransactions_per_field

    def _create_records(
        self,
        ctx: RelationalContext,
    ) -> Many2ManyUpdatesOnCreateCallback | Many2ManyUpdatesOnUpdateCallback:

        # Obtención del campo many2one
        many2one_field = self._strc.get_related_field_name(ctx.model_name, ctx.field_name)

        # Creación de función de subtransacciones por tipo
        def subtransactions_per_type(parent_record_ids: RecordIDs) -> None:
            # Obtención de la ID del registro
            [ parent_record_id ] = parent_record_ids
            # Iteración por cada colección de datos de comando
            for ( data, ) in ctx.subtransactions_data['create']:
                # Se asegura el tipo de dato
                data = self._main._preprocess.convert_to_list(data)
                # Iteración por cada registro de datos
                for record in data:
                    # Se registra la ID del registro padre
                    record[many2one_field] = parent_record_id

                # Creación de registros
                self._main.create(
                    self._main._ROOT_USER,
                    ctx.related_model_name,
                    data,
                )

        # Creación de función envuelta
        wrapped_subtransactions_per_type = self._m_wrapping.create_postcallback(subtransactions_per_type, ctx)

        return wrapped_subtransactions_per_type

    def _update_records(
        self,
        ctx: RelationalContext,
    ) -> Many2ManyUpdatesOnCreateCallback | Many2ManyUpdatesOnUpdateCallback:

        # Creación de función de subtransacciones por tipo
        def subtransactions_per_type(_: RecordIDs) -> None:
            # Iteración por cada subtransacción
            for ( record_ids, data ) in ctx.subtransactions_data['update']:
                # Actualización de registros
                self._main.update(
                    self._main._ROOT_USER,
                    ctx.related_model_name,
                    record_ids,
                    data,
                )

        # Creación de función envuelta
        wrapped_subtransactions_per_type = self._m_wrapping.create_postcallback(subtransactions_per_type, ctx)

        return wrapped_subtransactions_per_type

    def _delete_records(
        self,
        ctx: RelationalContext,
    ) -> Many2ManyUpdatesOnCreateCallback | Many2ManyUpdatesOnUpdateCallback:

        # Creación de función de subtransacciones por tipo
        def subtransactions_per_type(_: RecordIDs) -> None:
            # Iteración por cada subtransacción
            for ( record_ids, ) in ctx.subtransactions_data['delete']:
                # Eliminación de registros
                self._main.delete(
                    self._main._ROOT_USER,
                    ctx.related_model_name,
                    record_ids
                )

        # Creación de función envuelta
        wrapped_subtransactions_per_type = self._m_wrapping.create_postcallback(subtransactions_per_type, ctx)

        return wrapped_subtransactions_per_type

    def _add_records(
        self,
        ctx: RelationalContext,
    ) -> Many2ManyUpdatesOnCreateCallback | Many2ManyUpdatesOnUpdateCallback:

        # Obtención del campo many2one
        many2one_field = self._strc.get_related_field_name(ctx.model_name, ctx.field_name)

        # Creación de función de subtransacciones por tipo
        def subtransactions_per_type(record_ids: RecordIDs) -> None:
            # Obtención de la ID del registro
            [ record_id ] = record_ids
            # Iteración por cada subtransacción
            for ( record_ids, ) in ctx.subtransactions_data['add']:
                # Se modifica la ID a la que los registros hijos referencían
                self._main.update(
                    self._main._ROOT_USER,
                    ctx.related_model_name,
                    record_ids,
                    {many2one_field: record_id}
                )

        # Creación de función envuelta
        wrapped_subtransactions_per_type = self._m_wrapping.create_postcallback(subtransactions_per_type, ctx)

        return wrapped_subtransactions_per_type

    def _unlink_records(
        self,
        ctx: RelationalContext,
    ) -> Many2ManyUpdatesOnCreateCallback | Many2ManyUpdatesOnUpdateCallback:

        # Obtención del campo many2one
        many2one_field = self._strc.get_related_field_name(ctx.model_name, ctx.field_name)

        # Creación de función de subtransacciones por tipo
        def subtransactions_per_type(_: RecordIDs) -> None:
            # Iteración por cada subtransacción
            for ( record_ids, ) in ctx.subtransactions_data['unlink']:
                # Se elimina la referencia
                self._main.update(
                    self._main._ROOT_USER,
                    ctx.related_model_name,
                    record_ids,
                    {many2one_field: None},
                )

        # Creación de función envuelta
        wrapped_subtransactions_per_type = self._m_wrapping.create_postcallback(subtransactions_per_type, ctx)

        return wrapped_subtransactions_per_type

    def _clean_records(
        self,
        ctx: RelationalContext,
    ) -> Many2ManyUpdatesOnCreateCallback | Many2ManyUpdatesOnUpdateCallback:

        # Obtención del campo many2one
        many2one_field = self._strc.get_related_field_name(ctx.model_name, ctx.field_name)

        # Creación de función de subtransacciones por tipo
        def subtransactions_per_type(record_ids: list[int]):
            # Iteración por cada subtransacción
            for _ in ctx.subtransactions_data['clean']:
                # Iteración por cada ID de registro
                for record_id in record_ids:
                    # Obtención de las IDs referenciadas
                    children_record_ids = self._main.get_value(
                        self._main._ROOT_USER,
                        ctx.model_name,
                        record_id,
                        ctx.field_name
                    )

                    # Se elimina la referenciación
                    self._main.update(
                        self._main._ROOT_USER,
                        ctx.related_model_name,
                        children_record_ids,
                        {many2one_field: None}
                    )

        # Creación de función envuelta
        wrapped_subtransactions_per_type = self._m_wrapping.create_postcallback(subtransactions_per_type, ctx)

        return wrapped_subtransactions_per_type

    def _replace_records(
        self,
        ctx: RelationalContext,
    ) -> Many2ManyUpdatesOnCreateCallback | Many2ManyUpdatesOnUpdateCallback:

        # Obtención del campo many2one
        many2one_field = self._strc.get_related_field_name(ctx.model_name, ctx.field_name)

        # Creación de función de subtransacciones por tipo
        def subtransactions_per_type(parent_record_ids: list[int]):
            # Obtención de la ID del registro
            [ parent_record_id ] = parent_record_ids
            # Iteración por cada subtransacción
            for ( record_ids, ) in ctx.subtransactions_data['replace']:
                # Obtención de las IDs referenciadas
                children_record_ids = self._main.get_value(
                    self._main._ROOT_USER,
                    ctx.model_name,
                    parent_record_id,
                    ctx.field_name
                )

                # Se elimina la referenciación
                self._main.update(
                    self._main._ROOT_USER,
                    ctx.related_model_name,
                    children_record_ids,
                    {many2one_field: None}
                )

                # Se elimina la referenciación
                self._main.update(
                    self._main._ROOT_USER,
                    ctx.related_model_name,
                    record_ids,
                    {many2one_field: parent_record_id}
                )

        # Creación de función envuelta
        wrapped_subtransactions_per_type = self._m_wrapping.create_postcallback(subtransactions_per_type, ctx)

        return wrapped_subtransactions_per_type

    def _initialize_subtransactions_map(
        self,
    ) -> None:

        # Se crea el mapa de subtransacciones
        self._subtransactions_map = {
            'create': self._create_records,
            'update': self._update_records,
            'add': self._add_records,
            'unlink': self._unlink_records,
            'delete': self._delete_records,
            'clean': self._clean_records,
            'replace': self._replace_records,
        }
