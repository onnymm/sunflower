from ..._module_types import NewRecord
from ..._constants import (
    FIELD_NAME,
    MODEL_ID,
)

DEFAULT_FIELD_TEMPLATE: dict[str, NewRecord.ModelField] = {
    FIELD_NAME.CREATE_UID: {
        'label': 'Creado por',
        'name': FIELD_NAME.CREATE_UID,
        'ttype': 'many2one',
        'nullable': True,
        'related_model_id': MODEL_ID.BASE_USERS,
    },
    FIELD_NAME.WRITE_UID: {
        'label': 'Modificado por',
        'name': FIELD_NAME.WRITE_UID,
        'ttype': 'many2one',
        'nullable': True,
        'related_model_id': MODEL_ID.BASE_USERS,
    },
    FIELD_NAME.SEQUENCE: {
        'label': 'Secuencia',
        'name': FIELD_NAME.SEQUENCE,
        'ttype': 'integer',
    },
    FIELD_NAME.USER_ID: {
        'label': 'Usuario',
        'name': FIELD_NAME.USER_ID,
        'ttype': 'many2one',
        'nullable': True,
        'related_model_id': MODEL_ID.BASE_USERS,
    },
}

UID_FIELDS = [
    FIELD_NAME.CREATE_UID,
    FIELD_NAME.WRITE_UID,
]
