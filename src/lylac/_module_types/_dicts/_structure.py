from typing import TypedDict
from sqlalchemy.orm.decl_api import DeclarativeBase
from .._base_categories import (
    ModelName,
    TTypeName,
)

class FieldProperties(TypedDict):
    """
    ### Propiedades de campo
    Diccionario que almacena el tipo de dato y la relación de un campo.
    >>> {
    >>>     'ttype': 'many2one',
    >>>     'relation': 'base.users',
    >>> }
    """
    ttype: TTypeName
    """
    #### Tipo de dato en campo de modelo en la base de datos
    Tipo de dato válido en un campo de un modelo de la base de datos.
    - `'integer'`: Entero
    - `'char'`: Cadena de texto
    - `'float'`: Flotante
    - `'boolean'`: Booleano
    - `'date'`: Fecha
    - `'datetime'`: Fecha y hora
    - `'time'`: Hora
    - `'file'`: Archivo binario
    - `'text'`: Texto largo
    - `'selection'`: Selección
    - `'many2one'`: Muchos a uno
    - `'one2many'`: Uno a muchos
    - `'many2many'`: Muchos a muchos
    """
    related_model: ModelName
    """
    #### Modelo relacionado
    Modelo de la base de datos relacionado al campo.

    Nombres disponibles:
    - `'base.model'`: Modelos
    - `'base.model.field'`: Campos
    - `'base.model.field.selection'`: Valores de selección
    - `'base.users'`: Usuarios
    """
    related_field: str
    """
    #### Campo relacionado
    Nombre del campo relacionado.
    """
    selection_values: list[str]
    """
    #### Valores de selección
    Valores de selección si el tipo de dato del campo es `'selection'`.
    """
    is_computed: bool
    """
    #### Es campo computado
    Valor que indica si el valor del campo debe obtenerse directamente desde un registro
    en la base de datos o calcularse en base a otros campos.
    """

class ModelMap(TypedDict):
    """
    ### Mapa de atributos de modelo
    Este tipo de dato almacena la información básica que define la estructura de un
    modelo almacenado en una instancia Lylac.
    >>> {
    >>>     'model': <ModelInstance>,
    >>>     'fields': {
    >>>         'id': {
    >>>             'ttype': 'integer',
    >>>             'related_model': None,
    >>>             'related_field': None,
    >>>         },
    >>>         'write_uid': {
    >>>             'ttype': 'many2one',
    >>>             'related_model': 'base.users',
    >>>             'related_field': None,
    >>>         },
    >>>         'category_ids': {
    >>>             'ttype': 'one2many',
    >>>             'related_model': 'product.category',
    >>>             'related_field': 'product_id',
    >>>         },
    >>>         ...
    >>>     },
    >>> }
    """
    model: type[DeclarativeBase]
    """Modelo SQLAlchemy de la tabla"""
    fields: dict[str, FieldProperties]
    """
    Diccionario que almacena el tipo de dato y la relación de un campo.
    >>> {
    >>>     'many2one',
    >>>     'base.users',
    >>> }
    """
