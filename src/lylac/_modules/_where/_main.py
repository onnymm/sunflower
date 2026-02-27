from typing import (
    Any,
    overload,
)
from sqlalchemy import (
    Select,
    Update,
    and_,
    not_,
    or_,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.elements import (
    BinaryExpression,
    BooleanClauseList,
)
from ..._core.modules import Where_Core
from ..._core.main import _Lylac_Core
from ..._constants import MESSAGES
from ...errors import MalformedCriteriaError
from ..._module_types import (
    _T,
    CriteriaStructure,
    TripletStructure,
    ComparisonOperator,
    LogicOperator,
)
from ._submodule_types import (
    ComparisonCallback,
    ConditionUnionCallback,
)

class Where(Where_Core):

    _comparison_operation: dict[ComparisonOperator, ComparisonCallback] = {
        '=': lambda field, value: field == value,
        '!=': lambda field, value: field != value,
        '>': lambda field, value: field > value,
        '>=': lambda field, value: field >= value,
        '<': lambda field, value: field < value,
        '<=': lambda field, value: field <= value,
        '><': lambda field, value: field.between(value[0], value[1]),
        'in': lambda field, value: field.in_(value),
        'not in': lambda field, value: field.not_in(value),
        'ilike': lambda field, value: field.contains(value),
        'not ilike': lambda field, value: not_(field.contains(value)),
        '~': lambda field, value: field.regexp_match(value),
        '~*': lambda field, value: field.regexp_match(value, 'i'),
    }

    # Operaciones lógicas
    _logic_operation: dict[LogicOperator, ConditionUnionCallback] = {
        '|': lambda condition_1, condition_2: or_(condition_1, condition_2),
        '&': lambda condition_1, condition_2: and_(condition_1, condition_2),
    }

    def __init__(
        self,
        instance: _Lylac_Core,
    ) -> None:

        # Asignación de la instancia propietaria
        self._main = instance

        # Asignación de módulo de modelos
        self._models = instance._models

    @overload
    def add_query(
        self,
        stmt: Select[_T],
        model_model: type[DeclarativeBase],
        search_criteria: CriteriaStructure,
    ) -> Select[_T]:
        ...

    @overload
    def add_query(
        self,
        stmt: Update[_T],
        model_model: type[DeclarativeBase],
        search_criteria: CriteriaStructure,
    ) -> Update[_T]:
        ...

    def add_query(
        self,
        stmt: Select[_T] | Update[_T],
        model_model: type[DeclarativeBase],
        search_criteria: CriteriaStructure,
    ):

        # Creación del segmento WHERE en caso de haberlo
        if len(search_criteria) > 0:

            # Creación del query where
            query = self.build_where(model_model, search_criteria)

            # Conversión del query SQL
            stmt = stmt.where(query)

        # Retorno de la sentencia SQL
        return stmt

    def build_where(
        self,
        model_model: type[DeclarativeBase],
        search_criteria: CriteriaStructure,
    ) -> BinaryExpression:

        # Se crea una copia del criterio de búsqueda
        search_criteria = search_criteria.copy()
        # Si el criterio de búsqueda solo contiene una tripleta...
        if len(search_criteria) == 1:
            # Destructuración de la tripleta
            [ triplet ] = search_criteria
            # Procesamiento de la tripleta
            expression = self._create_individual_query(model_model, triplet)

            return expression

        # Si el criterio de búsqueda tiene 2 elementos de longitud...
        elif len(search_criteria) == 2:
            # Se lanza un error de estructura de búsqueda mal formada
            raise MalformedCriteriaError(MESSAGES.INVALID_STRUCTURE.SEARCH_CRITERIA)

        # Si el criterio de búsqueda contiene más de un elemento...
        else:
            # Procesamiento de todas las tripletas
            search_criteria = self._evaluate_triplets(model_model, search_criteria)
            # Obtención de la expresión final
            expression = self._merge_expressions(search_criteria)

            return expression

    def _evaluate_triplets(
        self,
        model_model: type[DeclarativeBase],
        search_criteria: CriteriaStructure,
    ) -> list[LogicOperator, BinaryExpression]:

        # Se recorren todas las posiciones de la lista
        for index in range(len(search_criteria)):
            # Obtención del elemento en posición i
            item = search_criteria[index]
            # Evaluación de si el elemento es tripleta
            is_triplet = self._is_triplet(item)
            # Si el elemento es tripleta...
            if is_triplet:
                # Creación de expresión binaria
                expression = self._create_individual_query(model_model, item)
                # Reasignación del elemento en la posición i
                search_criteria[index] = expression

        return search_criteria

    def _merge_expressions(
        self,
        expressions: list[BinaryExpression, LogicOperator],
    ) -> BinaryExpression:

        # Ciclo indefinido hasta que se resuelva la condición
        while len(expressions) > 2:
            # Indicador de combinación de expresiones encontrada
            found_combination = False
            # Se recorre cada posición de la lista de expresiones y operadores
            for index in range( len(expressions) - 2 ):
                # Destructuración de los elementos adyacentes
                [ item_a, item_b, item_c ] = expressions[index:index + 3]
                # Evaluación de si los elementos forman una expresión combinada
                is_combined_expression = self._is_combined_expression(item_a, item_b, item_c)
                # Si los elementos forman una expressión combinada...
                if is_combined_expression:
                    # Reasignación de variables
                    ( operator, expression_1, expression_2 ) = (item_a, item_b, item_c)
                    # Se unen las expresiones
                    expression_result = self._logic_operation[operator](expression_1, expression_2)
                    # Reasignación de la expresión resultante
                    expressions = expressions[:index] + [expression_result] + expressions[index + 3:]
                    # Se cambia el indicador de combinación encontrada a verdadero
                    found_combination = True
                    # Se termina el ciclo
                    break

            # Si al terminar el ciclo no hubo combinación encontrada...
            if not found_combination:
                # Si el ciclo se termina y no se encontró una combinación de expresiones se lanza un error
                raise MalformedCriteriaError(MESSAGES.INVALID_STRUCTURE.SEARCH_CRITERIA)

        # Obtención de la expresión resultante
        [ resolution ] = expressions

        return resolution

    def _is_triplet(
        self, value: Any
    ) -> bool:
        """
        ## Evaluación de posible tripleta de condición
        Esta función evalúa si el valor provisto es una tupla o una lista de
        3 valores que puede ser convertida a un query SQL.
        """

        # Evaluación de si el elemento es tupla
        is_tuple = isinstance(value, tuple)
        # Evaluación de si el elemento es lista
        is_list = isinstance(value, list)
        # Evaluación de si el elemento tiene longitud de 3
        has_right_length = len(value) == 3

        # Resolución de si el elemento es una tripleta
        is_triplet = (is_tuple or is_list) and has_right_length

        return is_triplet

    def _create_individual_query(
        self,
        model_model: type[DeclarativeBase],
        fragment: TripletStructure
    ) -> BinaryExpression:

        # Destructuración de valores
        ( field_instance, op, value ) = fragment

        # Obtención de la instancia del campo a usar
        field_instance = self._models.get_model_field(model_model, field_instance)

        # Retorno de la evaluación
        return self._comparison_operation[op](field_instance, value)

    def _is_combined_expression(
        self,
        item_a: LogicOperator | BinaryExpression,
        item_b: LogicOperator | BinaryExpression,
        item_c: LogicOperator | BinaryExpression,
    ) -> bool:

        # Evaluación de si el primer elemento es un operador lógico
        is_a_logic_operator = item_a in ['&', '|']
        # Evaluación de si el segundo elemento es una expresión binaria
        is_b_binary_expression = self._is_expression(item_b)
        # Evaluación de si el tercer elemento es una expresión binaria
        is_c_binary_expression = self._is_expression(item_c)

        # Resolución de evaluación
        resolution = is_a_logic_operator and is_b_binary_expression and is_c_binary_expression

        return resolution

    def _is_expression(
        self,
        item: BinaryExpression | BooleanClauseList,
    ) -> bool:
        
        # Evaluación de si el elemento es una cláusula booleana
        is_boolean_clause = isinstance(item, BooleanClauseList)
        # Evaluación de si el elemento es una expresión binaria
        is_binary_expression = isinstance(item, BinaryExpression)

        # Resolución
        resolution = is_boolean_clause or is_binary_expression

        return resolution
