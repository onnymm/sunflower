from typing import (
    Any,
    Callable,
    Optional,
)
from sqlalchemy import (
    Subquery,
    case,
    literal,
    select,
    cast as cast_,
    func,
)
from sqlalchemy.orm import aliased
from sqlalchemy.orm.decl_api import DeclarativeBase
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.elements import (
    BinaryExpression,
    BindParameter,
)
from .._constants import (
    FIELD_NAME,
    MESSAGES,
)
from .._core.main import _Lylac_Core
from .._module_types import (
    _ComputeContextCore,
    _SelectContextCore,
    CriteriaStructure,
    AggFunctionName,
    ComputedFieldCallback,
    ModelName,
    ToCast,
)

class ComputeContext(_ComputeContextCore):

    def __init__(
        self,
        model: ModelName | type[DeclarativeBase],
        select_context: _SelectContextCore,
        lylac_instance: _Lylac_Core,
    ) -> None:

        # Asignación de contexto de selección
        self._select_context = select_context
        # Asignación de módulo principal
        self._main = lylac_instance
        # Asignación de módulo de estructura interna
        self._strc = self._main._strc
        # Asignación de módulo de modelos
        self._models = self._main._models

        # Si el modelo provisto es una clase...
        if not isinstance(model, str):
            # Asignación de nombre de modelo en contexto
            self._model_name = self._models.get_model_name(model)
            # Obtención de clase de modelo
            self._model_model = model
        # Si el modelo provisto es un nombre...
        else:
            # Asignación de nombre de modelo en contexto
            self._model_name = model
            # Obtención de clase de modelo
            self._model_model = aliased( self._strc.get_model(model) )

    def __getitem__(
        self,
        field_name: str,
    ) -> InstrumentedAttribute[Any]:

        # Intento de obtención de cadena de campos
        fields_chain = field_name.split(self.FIELD_DIVISION)

        # Si existe cadena de campos...
        if len(fields_chain) > 1:
            # Obtención de la instancia de campo siguiendo la cadena de nombres de campo
            field_instance = self._get_related_field(self._model_model, fields_chain)
        # Si no existe cadena de campos...
        else:
            # Evaluación de si el campo es computado
            is_computed_field = self._strc.is_computed_field(self._model_name, field_name)
            # Si el campo es computado...
            if is_computed_field:
                # Obtención del campo computado o columna None si éste no tiene función de cómputo registrada
                field_instance = self._get_computed_field_for_another_computed_field(self._model_name, field_name)

            # Si el campo no es computado...
            else:
                # Obtención de la instancia de campo directamente desde el modelo
                field_instance = self._get_common_field_instance(field_name)

        return field_instance

    def concat(
        self,
        *args,
        sep: str = '',
    ):

        # Inicialización de lista de argumentos preprocesados
        preproccesed_args = []

        # Construcción de los argumentos con espacios incluidos
        for (index, arg) in enumerate(args):
            # Se añade el argumento en posición i
            preproccesed_args.append(arg)
            # Si el índice no es el último...
            if index != ( len(args) - 1 ):
                # Se añade un separador
                preproccesed_args.append(sep)

        # Uso de la función de concatenación
        field_instance = func.concat(*preproccesed_args)

        return field_instance

    def case(
        self,
        *args: tuple[BinaryExpression, Any],
        default: Any = None,
    ) -> InstrumentedAttribute:

        # Creación de valor condicional en instancia de campo
        field_instance = case(
            *args,
            else_= default
        )

        return field_instance

    def agg(
        self,
        composed_field_name: str,
        aggregation_function: AggFunctionName,
        search_criteria: CriteriaStructure = [],
    ) -> InstrumentedAttribute:

        # Obtención de la función de agregación a usar
        aggregation_callback_to_apply = self.aggregation_callbacks_map[aggregation_function]
        # Obtención del campo relacional y el campo para obtener el valor de agregación
        ( relational_field_name, value_field_name ) = self._get_related_and_value_fields(composed_field_name)
        # Obtención de la instancia de campo calculada
        field_instance = self._compute_and_aggregate_relational_field(
            self._model_model,
            relational_field_name,
            value_field_name,
            aggregation_callback_to_apply,
            search_criteria,
        )

        return field_instance

    def cast(
        self,
        field: InstrumentedAttribute[Any],
        ttype: ToCast,
    ) -> InstrumentedAttribute[Any]:

        # Obtención del tipo a castear
        cast_to = self._to_cast_ttype[ttype]

        return cast_(field, cast_to)

    def replace(
        self,
        field: InstrumentedAttribute[str],
        i: str,
        o: str,
    ) -> InstrumentedAttribute[str]:

        # Reemplazo de texto
        replaced = func.replace(field, i, o)

        return replaced

    def _get_related_field(
        self,
        model_model: type[DeclarativeBase],
        fields_chain: list[str],
    ) -> InstrumentedAttribute[Any]:

        # Obtención del nombre del modelo del campo actual
        model_name = self._main._models.get_model_name(model_model)

        # Obtención del nombre del campo actual
        current_field_name = fields_chain[0]
        # Obtención del nombre del modelo relacionado
        related_model_name = self._strc.get_related_model_name(model_name, current_field_name)
        # Obtención del modelo relacionado
        related_model_model = aliased( self._strc.get_model(related_model_name) )

        # Obtención de la instancia del campo actual
        id_current_field_instance = self._main._index[model_model][current_field_name]

        # Obtención del nombre del campo siguiente
        next_field_name = fields_chain[1]

        # Si hay más campos por accesar...
        if len(fields_chain) > 2:
            # Se añade el outerjoin
            self._add_join(id_current_field_instance, related_model_model)
            # Se accede a ellos de forma recursiva para obtener la instancia de campo
            field_instance = self._get_related_field(
                related_model_model,
                fields_chain[1:].copy(),
            )
        # Si es el último campo por accesar...
        else:
            # Evaluación de si el campo es computado
            is_computed_field = self._strc.is_computed_field(related_model_name, next_field_name)
            # Si el campo es computado...
            if is_computed_field:
                # Obtención del campo computado
                field_instance = self._get_computed_field_from_many2one(model_model, current_field_name, related_model_name, next_field_name)
            # Si el campo no es computado...
            else:
                # Se añade el outerjoin
                self._add_join(id_current_field_instance, related_model_model)
                # Obtención de la instancia del campo desde el modelo relacionado
                field_instance = self._get_common_field_instance(next_field_name, related_model_model)

        return field_instance

    def _get_computed_field_for_another_computed_field(
        self,
        model_name: ModelName,
        field_name: str,
    ) -> InstrumentedAttribute[Any] | BindParameter[None]:

        # Si el campo es el nombre visible del modelo...
        if field_name == FIELD_NAME.DISPLAY_NAME:
            # Obtención de la instancia de campo de nombre visible
            field_instance = self._get_display_name_field(model_name)
        # Si el campo es distinto al nombre visible...
        else:
            # Si existe una función para computar el campo...
            if self._computation_callback_exists(model_name, field_name):
                # Obtención de la instancia del campo
                field_computation_callback = self._get_computation_callback(field_name)
                # Inicialización de la instancia de cómputo de campo
                compute_ctx = ComputeContext(self._model_name, self._select_context, self._main)
                # Obtención de la instancia de campo
                field_instance = field_computation_callback(compute_ctx)
            # Si no existe una función para computar el campo...
            else:
                # Creación de una columna de NULL
                field_instance = literal(None)

        return field_instance

    def _get_common_field_instance(
        self,
        field_name: str,
        model_model: Optional[type[DeclarativeBase]] = None,
    ) -> InstrumentedAttribute[Any]:

        # Si no fue provisto un modelo...
        if model_model is None:
            # Se usa el modelo de la instancia
            model_model = self._model_model

        # Obteción de la instancia de campo
        field_instance = self._main._index[model_model][field_name]

        return field_instance

    def _get_related_and_value_fields(
        self,
        composed_field_name: str,
    ) -> tuple[str, str]:

        # Si existe una división de campos...
        if self.FIELD_DIVISION in composed_field_name:
            # Se obtienen los campos
            splitted_fields = composed_field_name.split(self.FIELD_DIVISION)
            # Si la división no es de dos campos
            if len(splitted_fields) != 2:
                # Se arroja un error de desbordamiento
                raise OverflowError(MESSAGES.TRANSACTION.FIELDS_OVERFLOW)
            else:
                # Obtención del campo relacional y campo de valor
                ( relational_field_name, value_field_name ) = splitted_fields
        # Si no existe una división de campos...
        else:
            # Se usa el campo de ID de la tabla relacionada como campo de ID
            ( relational_field_name, value_field_name ) = ( composed_field_name, FIELD_NAME.ID )

        return ( relational_field_name, value_field_name )

    def _compute_and_aggregate_relational_field(
        self,
        model_model: type[DeclarativeBase],
        relational_field_name: str,
        value_field_name: str,
        aggregation_callback: Callable[[InstrumentedAttribute], Any],
        search_criteria: CriteriaStructure = [],
    ) -> InstrumentedAttribute:

        # Obtención del nombre del modelo
        model_name = model_model.__tablename__.replace('_', '.')
        # Obtención del nombre del modelo relacionado
        related_model_name = self._strc.get_related_model_name(model_name, relational_field_name)

        # Obtención de la instancia de campo de ID de tabla padre
        id_field_instance = self._main._index[model_model][FIELD_NAME.ID]
        # Creación de un alias de la instancia de campo de ID de tabla padre para evitar colisiones
        id_field_instance_alias = id_field_instance.label(self.ID_ALIAS)

        # Evaluación de si el campo a usar en el cálculo es computado
        value_field_instance_is_computed = self._strc.is_computed_field(related_model_name, value_field_name)
        # Obtención del nombre del campo que relaciona a la tabla padre
        related_field_name = self._strc.get_related_field_name(model_name, relational_field_name)

        # Si el campo a usar en el cálculo es computado...
        if value_field_instance_is_computed:
            # Se crea un subquery para obtener el campo computado resultante
            ( computation_stmt, _ ) = self._main._select.build(related_model_name)
            # Se convierte el query de cómputo a subquery
            computation_stmt = computation_stmt.subquery()
            # Obtención de la instancia del campo que relaciona a la tabla padre
            related_field_instance = self._main._index[computation_stmt.c][related_field_name]
            # Obtención de la instancia de campo de valor del modelo relacionado
            related_model_model__value_field = self._main._index[computation_stmt.c][value_field_name]
            # Se asigna el objetivo de JOIN
            join_target = computation_stmt
        # Si el campo a usar en el cálculo no es computado...
        else:
            # Obtención del modelo relacionado
            related_model_model = aliased( self._strc.get_model(related_model_name) )
            # Se asigna el objetivo de JOIN
            join_target = related_model_model
            # Obtención de la instancia de campo de valor del modelo relacionado
            related_model_model__value_field = self._main._index[join_target][value_field_name]

            # Obtención de la instancia del campo que relaciona a la tabla padre
            related_field_instance = self._main._index[join_target][related_field_name]

        stmt = (
            # Selección de campos a usar
            select(
                # Uso del campo de alias de ID
                id_field_instance_alias,
                # Campo agregado
                (
                    # Uso de función de agregación seleccionada
                    aggregation_callback(related_model_model__value_field)
                    # Campo con etiqueta para ser extraído del subquery
                    .label(value_field_name)
                ),
            )
            # Especificación del modelo a usar para la selección de columnas
            .select_from(model_model)
            # OUTER JOIN con la tabla referenciada
            .outerjoin(
                join_target,
                id_field_instance == related_field_instance
            )
        )

        # Si un criterio de búsqueda fue provisto...
        if search_criteria:
            # Se añade el fragmento de query para filtrar los registros a usar
            stmt = self._main._where.add_query(
                stmt,
                join_target,
                search_criteria,
            )

        # Se genera la agrupación por el campo de ID y se convierte el query a subquery
        stmt = (
            stmt
            # Agrupamiento de registros por ID
            .group_by(id_field_instance)
            # Conversión a subquery
            .subquery()
        )

        # Se añade el OUTER JOIN al contexto de selección
        self._select_context.add_outerjoin(
            stmt,
            id_field_instance == getattr(stmt.c, self.ID_ALIAS)
        )

        # Obtención de la instancia a retornar
        field_instance = self._main._index[stmt.c][value_field_name]

        # Obtención del tipo de dato del campo
        field_ttype = self._strc.get_field_ttype(related_model_name, value_field_name)

        # Reemplazo de valores None por 0
        processed_field_instance = case(
            (field_instance == None, self._zero_value[field_ttype]),
            else_= field_instance,
        )

        return processed_field_instance

    def _get_computed_field_from_many2one(
        self,
        model_model: type[DeclarativeBase],
        field_name: str,
        related_model_name: ModelName,
        computed_related_field_name: str,
    ) -> InstrumentedAttribute[Any]:

        # Obtención del subquery
        ( computation_stmt, _ ) = (
            self._main._select.build(
                related_model_name,
                [computed_related_field_name]
            )
        )
        # Se convierte el query de cómputo a subquery
        computation_stmt = computation_stmt.subquery()

        # Obtención de la instancia de campo computado del modelo relacionado
        computed_field_instance = self._main._index[computation_stmt.c][computed_related_field_name]
        # Obtención de la instancia del modelo que relaciona desde la tabla padre
        id_field_instance = self._main._index[model_model][field_name]
        # Se añade el JOIN con el subquery de campo computado
        self._add_join(id_field_instance, computation_stmt, True)

        return computed_field_instance

    def _add_join(
        self,
        id_current_field_instance: InstrumentedAttribute,
        related_model_model: type[DeclarativeBase] | Subquery,
        subquery: bool = False,
    ) -> None:

        # Si el modelo es subquery...
        if subquery:
            content_target = related_model_model.c
        else:
            content_target = related_model_model

        # Obtención de instancia del campo de ID del modelo relacionado
        id_related_field = self._main._index[content_target][FIELD_NAME.ID]
        # Creación de unión ON
        on = id_current_field_instance == id_related_field
        # Se añade el JOIN
        self._select_context.add_outerjoin(related_model_model, on)

    def _get_display_name_field(
        self,
        model_name: ModelName,
    ) -> InstrumentedAttribute[str]:

        # Si existe una función para computar el nombre visible...
        if self._computation_callback_exists(model_name, FIELD_NAME.DISPLAY_NAME):
            # Obtención de la instancia del campo
            field_computation_callback = self._get_computation_callback(FIELD_NAME.DISPLAY_NAME)
            # Inicialización de la instancia de cómputo de campo
            compute_ctx = ComputeContext(self._model_model, self._select_context, self._main)
            # Obtención de la instancia de campo
            field_instance = field_computation_callback(compute_ctx).label(FIELD_NAME.DISPLAY_NAME)
        # Si no existe una función para computar el nombre visible...
        else:
            # Obtención de la instancia de campo de nombre
            field_instance = self._get_default_display_name()

        return field_instance

    def _computation_callback_exists(
        self,
        model_name: ModelName,
        field_name: str,
    ) -> bool:

        # Evaluación de existencia de función para realizar cómputo
        callback_exists = field_name in self._main._compute.hub[model_name].keys()

        return callback_exists

    def _get_computation_callback(
        self,
        field_name: str,
    ) -> ComputedFieldCallback:

        # Obtención de la función de cómputo del campo
        computation_callback = self._main._compute.hub[self._model_name][field_name]

        return computation_callback

    def _get_default_display_name(
        self,
    ) -> None:

        # Obtención de instancia de ID del modelo
        id_field_instance = self._main._index[self._model_model][FIELD_NAME.ID]
        # Obtención de instancia de nombre del registro
        name_field_instance = self._main._index[self._model_model][FIELD_NAME.NAME]

        # Creación de query conditional
        field_instance = case(
            (name_field_instance != None, name_field_instance),
            else_= func.concat(id_field_instance, ', ', self._model_name)
        )

        return field_instance
