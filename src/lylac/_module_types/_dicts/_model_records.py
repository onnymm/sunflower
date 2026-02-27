from typing import TypedDict, Literal
from .._base_categories import (
    ModelName,
    State,
    TTypeName,
)

class BaseRecordData(TypedDict):
    id: int
    """
    ID del registro
    """
    name: str
    """
    Nombre del registro
    """
    create_date: str
    """
    Fecha de creación
    """
    write_date: str
    """
    Fecha de modificación
    """
    create_uid: int
    """
    Usuario de creación
    """
    write_uid: int
    """
    Usuario de modificación
    """

class _HasLabel(TypedDict):
    label: str
    """
    Etiqueta
    """

class _HasState(TypedDict):
    state: State
    """
    Tipo
    """

class _HasModelID(TypedDict):
    model_id: int
    """
    ID de modelo
    """

class _HasTType(TypedDict):
    ttype: TTypeName

class _HasActive(TypedDict):
    active: bool
    """
    Está activo
    """

class _HasSync(TypedDict):
    sync: bool
    """
    Sincronizar
    """

class ModelRecordData:
    """
    #### Datos de registros en la base de datos
    Tipados de datos de registros de diferentes modelos en la base de datos.

    >>> class ModelRecordData:
    >>>     # Datos de modelos
    >>>     class BaseModel_(TypedDict...):
    >>>         ...
    >>>     # Datos de campos
    >>>     class BaseModelField(TypedDict...):
    >>>         ...
    >>>     # Datos de valores de selección de campos
    >>>     class BaseModelFieldSelection(TypedDict...):
    >>>         ...
    >>>     # Datos de usuarios
    >>>     class BaseUsers(TypedDict...):
    >>>         ...
    """

    class BaseModel_(
        BaseRecordData,
        _HasLabel,
        _HasState,
    ):
        """
        Datos de modelo
        >>> {
        >>>     # ID del registro
        >>>     'id': 1,
        >>>     # Nombre del registro
        >>>     'name': 'base_model',
        >>>     # Fecha de creación
        >>>     'create_date': '2025-07-01-10:00:00',
        >>>     # Fecha de modificación
        >>>     'write_date': '2025-07-01-10:00:00',
        >>>     # Usuario de creación
        >>>     'create_uid': 1,
        >>>     # Usuario de modificación
        >>>     'write_uid': 1,
        >>>     # Etiqueta
        >>>     'label': 'Modelos',
        >>>     # Tipo
        >>>     'state': 'base',
        >>>     # Nombre del modelo
        >>>     'model': 'base.model',
        >>>     # Descripción
        >>>     'description': '...',
        >>>     # Campos
        >>>     'field_ids': [1, 2, 3, ...],
        >>>     # Campos relacionados al modelo
        >>>     'related_field_ids': [5, 8, ...],
        >>> }
        """
        model: ModelName
        """
        Nombre del modelo
        """
        description: str
        """
        Descripción
        """
        field_ids: list[int]
        """
        Campos del campo
        """
        related_field_ids: list[int]
        """
        Campos relacionados al modelo
        """

    class BaseModelField(
        BaseRecordData,
        _HasLabel,
        _HasState,
        _HasModelID,
        _HasTType,
    ):
        """
        Datos de campo
        >>> {
        >>>     # ID del registro
        >>>     'id': 1,
        >>>     # Nombre del registro
        >>>     'name': 'nullable',
        >>>     # Fecha de creación
        >>>     'create_date': '2025-07-01-10:00:00',
        >>>     # Fecha de modificación
        >>>     'write_date': '2025-07-01-10:00:00',
        >>>     # Usuario de creación
        >>>     'create_uid': 1,
        >>>     # Usuario de modificación
        >>>     'write_uid': 1,
        >>>     # Etiqueta
        >>>     'label': 'Puede ser nulo',
        >>>     # Tipo
        >>>     'state': 'base',
        >>>     # ID de modelo
        >>>     'model_id': 2,
        >>>     # Tipo de dato en campo
        >>>     'ttype': 'boolean',
        >>>     # Puede ser nulo
        >>>     'nullable': True,
        >>>     # Es requerido
        >>>     'is_required': False,
        >>>     # Valor predeterminado
        >>>     'default_value': None,
        >>>     # Es valor único
        >>>     'unique': False,
        >>>     # Información de ayuda
        >>>     'help_info': '...',
        >>>     # Modelo relacionado
        >>>     'related_model_id': None,
        >>>     # Campo relacionado
        >>>     'related_field': None,
        >>>     # Valores de selección
        >>>     'selection_ids': [],
        >>> }
        """
        nullable: bool
        """
        Puede ser nulo
        """
        is_required: bool
        """
        Es requerido
        """
        readonly: bool
        """
        Solo lectura
        """
        default_value: str
        """
        Valor predeterminado
        """
        unique: bool
        """
        Es valor único
        """
        help_info: str
        """
        Información de ayuda
        """
        related_model_id: int
        """
        Modelo relacionado
        """
        related_field: str
        """
        Campo relacionado
        """
        selection_ids: list[int]
        """
        Valores de selección
        """
        is_computed: bool
        """
        Es computado.
        """

    class BaseModelFieldSelection(
        BaseRecordData,
        _HasLabel,
    ):
        """
        Datos de valores de selección de campo
        >>> {
        >>>     # ID del registro
        >>>     'id': 2,
        >>>     # Nombre del registro
        >>>     'name': 'generic',
        >>>     # Fecha de creación
        >>>     'create_date': '2025-07-01-10:00:00',
        >>>     # Fecha de modificación
        >>>     'write_date': '2025-07-01-10:00:00',
        >>>     # Usuario de creación
        >>>     'create_uid': 1,
        >>>     # Usuario de modificación
        >>>     'write_uid': 1,
        >>>     # Etiqueta
        >>>     'label': 'Puede ser nulo',
        >>>     # ID de campo
        >>>     'field_id': 8,
        >>> }
        """
        field_id: int
        """
        ID de Campo
        """

    class BaseUsers(
        BaseRecordData,
        _HasActive,
        _HasSync,
    ):
        """
        Datos de usuario
        >>> {
        >>>     # ID del registro
        >>>     'id': 1,
        >>>     # Nombre del registro
        >>>     'name': 'iaCele',
        >>>     # Fecha de creación
        >>>     'create_date': '2025-07-01-10:00:00',
        >>>     # Fecha de modificación
        >>>     'write_date': '2025-07-01-10:00:00',
        >>>     # Usuario de creación
        >>>     'create_uid': 1,
        >>>     # Usuario de modificación
        >>>     'write_uid': 1,
        >>>     # Está activo
        >>>     'active': True,
        >>>     # Sincronizar
        >>>     'sync': False,
        >>>     # Nombre de usuario
        >>>     'login': 'iacele',
        >>>     # Contraseña
        >>>     'password': '...',
        >>> }
        """
        login: str
        """
        Nombre de usuario
        """
        password: int
        """
        Contraseña
        """
