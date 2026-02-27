from typing import (
    Optional,
    TypedDict,
)
from .._base_categories import (
    ModelName,
    TTypeName,
)

class NewRecord():
    """
    #### Nuevo registro
    Estructuras de diccionarios para la creación de nuevos registros en los modelos
    predeterminados de Lylac.

    Uso:
    >>> # Estructura de datos para la creación de un nuevo registro de modelo.
    >>> model: NewRecord.Model = {...}

    Los tipos disponibles son:
    - `Model`: Modelo
    - `ModelField`: Campo
    - `ModelFieldSelection`: Selección de campo
    - `User`: Usuario
    """

    class Model(TypedDict):
        """
        #### Nuevo registro de modelo
        Estructura del diccionario.
        >>> {
        >>>     # Nombre
        >>>     'name': 'my_model',
        >>>     # Nombre de modelo
        >>>     'model': 'my.model',
        >>>     # Etiqueta
        >>>     'label': 'Mi modelo',
        >>>     # Descripción
        >>>     'description': 'Modelo personalizado en la base de datos.'
        >>> }
        """
        name: str
        """
        #### Nombre
        Nombre del registro.
        """
        label: str
        """
        #### Etiqueta
        Etiqueta del registro.
        """
        model: ModelName
        """
        #### Nombre de modelo
        Nombre de modelo base de la base de datos.

        Nombres disponibles:
        - `'base.model'`: Modelos
        - `'base.model.field'`: Campos
        - `'base.model.field.selection'`: Valores de selección
        - `'base.users'`: Usuarios

        También se puede utilizar un nombre personalizado si es que el modelo ya existe
        en la base de datos.
        """
        description: str
        """
        #### Descripción
        Descripción del modelo.
        """

    class ModelField(TypedDict):
        """
        #### Nuevo registro de campo
        Estructura del diccionario.
        >>> {
        >>>     # Nombre
        >>>     'name': 'my_field',
        >>>     # Etiqueta
        >>>     'label': 'Mi campo',
        >>>     # Tipo de dato en campo de modelo en la base de datos
        >>>     'ttype': 'char',
        >>>     # ID de modelo
        >>>     'model_id': 5,
        >>>     # Valor predeterminado
        >>>     'default_value': 'Mi valor predeterminado',
        >>>     # Puede ser nulo
        >>>     'nullable': True,
        >>>     # Es único
        >>>     'unique': False,
        >>> }
        """
        name: str
        """
        #### Nombre
        Nombre del registro.
        """
        label: str
        """
        #### Etiqueta
        Etiqueta del registro.
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
        model_id: int
        """
        #### ID de modelo
        ID del registro del modelo a relacionar.
        """
        nullable: bool
        """
        #### Puede ser nulo
        Valor booleano que indica si este campo puede iniciarse como nulo en la
        creación de un nuevo registro en el modelo relacionado.
        """
        unique: bool
        """
        #### Es único
        Valor booleano que indica que el valor de este campo en los registros no puede
        existir repetido.
        """
        is_required: bool
        """
        #### Requerido
        Indicador de si el valor del campo es requerido en la creación del campo.
        """
        default_value: Optional[str]
        """
        #### Valor predeterminado
        Valor que se usará como predeterminado en caso de no especificarse un valor
        para el campo en la creación de un nuevo registro.
        """
        help_info: str | None
        """
        #### Información
        Información de ayuda para identificar el uso o la función de este campo.
        """
        related_model_id: int | None
        """
        #### ID de modelo relacionado
        ID del modelo relacionado en caso de haberlo. Para esto, el tipo de campo debe
        ser `many2one`.
        """

    class ModelFieldSelection(TypedDict):
        """
        Nuevo registro de selección de campo
        Estructura del diccionario.
        >>> {
        >>>     # Nombre
        >>>     'name': 'value_1',
        >>>     # Etiqueta
        >>>     'label': 'Valor 1',
        >>>     # ID de campo
        >>>     'field_id': 25,
        >>> }
        """
        name: str
        """
        #### Nombre
        Nombre del registro.
        """
        label: str
        """
        #### Etiqueta
        Etiqueta del registro.
        """
        field_id: int
        """
        #### ID de campo
        ID del campo relacionado.
        """

    class User(TypedDict):
        """
        #### Nuevo registro de usuario
        Estructura del diccionario.
        >>> {
        >>>     # Nombre
        >>>     'name': 'Onnymm',
        >>>     # Nombre de usuario
        >>>     'login': 'onnymm',
        >>>     # ID de Odoo
        >>>     'odoo_id': 5,
        >>>     # Sincronizar
        >>>     'sync': False,
        >>> }
        """
        name: str
        """
        #### Nombre
        Nombre del registro.
        """
        login: str
        """
        #### Nombre de usuario
        Nombre de usuario para inicio de sesión.
        """
        sync: bool
        """
        #### Sincronizar
        Valor que indica si este registro se sincronizará con datos externos.
        """
