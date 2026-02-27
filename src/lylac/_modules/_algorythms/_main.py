from typing import (
    Callable,
    Optional,
    overload,
)
from ..._core.modules import Algorythms_Core
from ..._core.main import _Lylac_Core
from ..._module_types import (
    _C,
    _E,
    _T,
)

class Algorythms(Algorythms_Core):

    def __init__(
        self,
        instance: _Lylac_Core,
    ) -> None:

        # Asignación de instancia principal
        self._main = instance

    @overload
    def find_duplicates(
        self,
        data: list[_T],
        extractor: Callable[[_T], _E] = lambda value: value,
        groupby: None = None,
    ) -> list[_E]:
        ...

    @overload
    def find_duplicates(
        self,
        data: list[_T],
        extractor: Callable[[_T], _E],
        groupby: Callable[[_T], _C],
    ) -> dict[_C, list[_E]]:
        ...

    def find_duplicates(
        self,
        data: list[_T],
        extractor: Callable[[_T], _E] = lambda value: value,
        groupby: Optional[ Callable[[_T], _C] ] = None,
    ) -> list[_E] | dict[_C, list[_E]]:

        # Inicialización de la función de categorización
        if groupby is None:
            classify = lambda _: True
        else:
            classify = groupby

        # Inicialización de colección de datos organizados
        classified_data = { classify(item): [] for item in data }

        # Inicialización de colección de datos duplicados
        duplicated_data = { classify(item): [] for item in data }

        # Clasificación por cada uno de los elementos
        for item in data:
            classified_data[ classify(item) ].append( extractor(item) )

        # Búsqueda de duplicados
        for category in classified_data:
            duplicated_data[category] = self._find_raw_duplicates( classified_data[category] )

        # Si no se proporcionó una función de clasificación...
        if groupby is None:
            # Se retorna una lista de resultados
            return duplicated_data[True]
        # Si una función de clasificación fue proporcionada...
        else:
            # Se retorna un diccionario agrupando los duplicados
            return duplicated_data

    def get_from(
        self,
        data: list[_T],
        condition: Callable[[_T], bool],
        value: Callable[[_T], _E] = lambda value: value,
    ) -> list[_E]:

        return [ value(item) for item in data if condition(item) ]

    def _find_raw_duplicates(
        self,
        data: list[_T],
    ) -> list[_T]:

        # Obtención de la cantidad de datos a revisar
        items_qty = len(data)

        # Inicialización de lista de duplicados a retornar
        duplicated: list[_T] = []

        # Si la cantidad de datos es menor o igual a 1 no hay suficientes datos para comparar
        if items_qty <= 1:
            return duplicated

        # Iteración controlada para reducir complejidad algorítmica
        for index_a in range(items_qty):
            for index_b in range(index_a + 1, items_qty):

                # Extracción de los valores a comparar
                item_a = data[index_a]
                item_b = data[index_b]

                # Si los valores son iguales
                if item_a == item_b:
                    # Se añade el elemento A a la lista de duplicados
                    duplicated.append(item_a)

        return duplicated
