from typing import Union

# Tipo de dato de valor para queries SQL
RecordValue = Union[
    int,
    float,
    str,
    bool,
    list[int],
    list[float],
    list[str],
    list[bool],
]
"""
#### Valor de registro
Este tipo de dato representa los tipos de dato válidos para diversos
argumentos de entrada en métodos del módulo así como en funcionamientos
internos, retornos en JSON y validaciones.
>>> # Tipos de dato individuales
>>> 5
>>> 2.8
>>> 'nombre'
>>> True
>>> # Listas de tipos de dato
>>> [1, 2, 3]
>>> [1.0, 3.5, 20.56]
>>> ['name', 'char', 'active']
>>> [False, True, True]
"""

# Datos para la creación de un objeto
RecordData = dict[str, RecordValue]
"""
#### Datos de registro
Datos que contienen los valores de campo de un registro en la base de datos.
Ejemplo:
>>> {
>>>     'name': 'Onnymm',
>>>     'password': ...,
>>>     'active': True,
>>> }
"""
