from typing import TypeVar

_M = TypeVar("_M")
"""
#### Nombre de modelo personalizado
Nombre de modelo personalizado
"""

_T = TypeVar("_T")
"""
#### Tipo de dato genérico
Tipo de dato genérico usado para declarar entradas y salidas dinámicas en
funciones:
>>> def do_something(param: _T) -> _T:
>>>     ...
>>> a = do_something(5) # `a` se tipa como entero
>>> b = do_something('Onnymm') # `b` se tipa como cadena de texto
>>> c = do_something(True) # `c` se tipa como booleano

Este tipo de dato también se puede usar para transformación de tipos de dato de
entradas y salidas:
>>> def get_first_item(iterable_object: list[_T]) -> _T:
>>>     return iterable_object[0]
>>> a = get_first_item([1, 2, 3]) # `a` se tipa como entero
>>> b = get_first_item(['uno', 'dos', 'tres']) # `b` se tipa como cadena de texto
>>> c = get_first_item([True, False]) # `c` se tipa como booleano
"""

_E = TypeVar('_E')
"""
#### Tipo de dato genérico
Tipo de dato usado para declarar un valor extraído de una colección de datos.
"""

_C = TypeVar('_C')
"""
#### Tipo de dato genérico
Tipo de dato usado para declarar un valor base para ser usado como criterio de
clasificación de grupos de datos.
"""

_I = TypeVar('_I')
"""
#### Tipo de dato genérico
Tipo de dato usado para declarar un valor del contenido de un iterable.
"""

ItemOrList = _I | list[_I]
"""
### Elemento o lista de elementos
Tipado que permite declarar que el tipo de dato es un elemento individual de
tipo `_T` o una lista de elementos del tipo `_T`.

Ejemplos:
>>> ItemOrList[int]
>>> # int | list[int]
>>> 
>>> ItemOrList[DataOnCreate]
>>> # DataOnCreate | list[DataOnCreate]
"""
