from ..._module_types import AutomationData

PRESET_AUTOMATIONS: list[AutomationData] = [

    # base.model
    # Creación de tabla en base de datos cuando un modelo se crea
    {
        'submodule': '_ddl',
        'callback': 'create_table',
        'model': 'base.model',
        'transaction': 'create',
        'criteria': [('state', '!=', 'base')],
        'fields': ['name', 'model'],
        'method': 'record',
    },
    # Registro de modelo de SQLAlchemy cuando un modelo de crea
    {
        'submodule': '_automations',
        'callback': 'register_new_model',
        'model': 'base.model',
        'transaction': 'create',
        'criteria': [('state', '!=', 'base')],
        'fields': ['model'],
        'method': 'record',
    },
    # Creación de los registros de campos base cuando un modelo se crea
    {
        'submodule': '_ddl',
        'callback': 'create_base_fields',
        'model': 'base.model',
        'transaction': 'create',
        'criteria': [('state', '!=', 'base')],
        'fields': ['id'],
        'method': 'record',
    },
    # Creación de los registros de campos predeterminados cuando un modelo se crea
    {
        'submodule': '_ddl',
        'callback': 'add_preset_fields',
        'model': 'base.model',
        'transaction': 'create',
        'criteria': [],
        'fields': ['id'],
        'method': 'record',
    },
    # Inicialización de campo de nombre visible cuando un modelo se crea
    {
        'submodule': '_ddl',
        'callback': 'initialize_display_name_field',
        'model': 'base.model',
        'transaction': 'create',
        'criteria': [('state', '!=', 'base')],
        'fields': [],
        'method': 'record',
    },
    # Inicialización de registro de validaciones de modelo cuando un modelo se crea
    {
        'submodule': '_validations',
        'callback': 'initialize_validations',
        'model': 'base.model',
        'transaction': 'create',
        'criteria': [],
        'fields': ['model'],
        'method': 'record',
    },
    # Eliminación de una tabla de base de datos cuando un modelo se elimina
    {
        'submodule': '_ddl',
        'callback': 'delete_table',
        'model': 'base.model',
        'transaction': 'delete',
        'criteria': [('state', '!=', 'base')],
        'fields': ['name', 'model'],
        'method': 'record',
    },
    # Eliminación de una columna de base de datos cuando un modelo se elimina
    {
        'submodule': '_ddl',
        'callback': 'delete_column',
        'model': 'base.model.field',
        'transaction': 'delete',
        'criteria': [('ttype', 'not in', ['one2many', 'many2many'])],
        'fields': ['name', 'model_id'],
        'method': 'record',
    },
    # Eliminación de registro de validaciones de modelo cuando un modelo se elimina
    {
        'submodule': '_validations',
        'callback': 'delete_validations',
        'model': 'base.model',
        'transaction': 'delete',
        'criteria': [],
        'fields': ['model'],
        'method': 'record',
    },
    # Inicialización de registro de acciones cuando un modelo se crea
    {
        'submodule': '_actions',
        'callback': 'register_model',
        'model': 'base.model',
        'transaction': 'create',
        'criteria': [],
        'fields': ['model'],
        'method': 'record',
    },
    # Eliminación de registro de acciones cuando un modelo se elimina
    {
        'submodule': '_actions',
        'callback': 'unregister_model',
        'model': 'base.model',
        'transaction': 'delete',
        'criteria': [],
        'fields': ['model'],
        'method': 'record',
    },
    # Registro de un modelo en el núcleo de campos computados cuando un registro se crea en la tabla de modelos
    {
        'submodule': '_compute',
        'callback': 'register_model',
        'model': 'base.model',
        'transaction': 'create',
        'criteria': [],
        'fields': ['model'],
        'method': 'record',
    },
    # Eliminación de un modelo en el núcleo de campos computados cuando un registro se elimina en la tabla de modelos
    {
        'submodule': '_compute',
        'callback': 'unregister_model',
        'model': 'base.model',
        'transaction': 'delete',
        'criteria': [],
        'fields': ['model'],
        'method': 'record',
    },

    # base.model.field
    # Creación de una columna de base de datos cuando un campo se crea
    {
        'submodule': '_ddl',
        'callback': 'create_column',
        'model': 'base.model.field',
        'transaction': 'create',
        'criteria': [
            '&',
                '&',
                    ('ttype', 'not in', ['one2many', 'many2many']),
                    '&',
                        ('state', '!=', 'base'),
                        ('name', 'not in', ['id', 'name', 'create_date', 'write_date']),
                ('is_computed', '=', False),
        ],
        'fields': [
            'name',
            'model_id',
            'label',
            'ttype',
            'nullable',
            'is_required',
            'unique',
            'default_value',
            'help_info',
            'related_model_id',
            'is_computed',
        ],
        'method': 'record',
    },
    # Creación de tabla de relación de campo many2many cuando un campo many2many se crea
    {
        'submodule': '_ddl',
        'callback': 'create_relation_table',
        'model': 'base.model.field',
        'transaction': 'create',
        'criteria': [('ttype', '=', 'many2many')],
        'fields': ['model_id', 'related_model_id'],
        'method': 'record',
    },
    # Registro de las propiedades de campo cuando un campo se crea
    {
        'submodule': '_strc',
        'callback': 'register_field_atts',
        'model': 'base.model.field',
        'transaction': 'create',
        'criteria': [
            '&',
                '|',
                    ('name', 'in', ['create_uid', 'write_uid']),
                    ('state', '!=', 'base'),
                ('is_computed', '=', False),
        ],
        'fields': [
            'name',
            'ttype',
            'model_id',
            'related_model_id',
            'related_field',
        ],
        'method': 'record',
    },
    # Eliminación de tabla de relación de campo many2many cuando un campo many2many se elimina
    {
        'submodule': '_ddl',
        'callback': 'delete_relation_table',
        'model': 'base.model.field',
        'transaction': 'delete',
        'criteria': [('ttype', '=', 'many2many')],
        'fields': ['name', 'model_id'],
        'method': 'record',
    },

    # base.model.field.selection
    # Actualización de los valores de selección de un campo de tipo de selección cuando un registro se crea en la tabla de valores de selección de campos
    {
        'submodule': '_ddl',
        'callback': 'update_selection_values_on_create',
        'model': 'base.model.field.selection',
        'transaction': 'create',
        'criteria': [],
        'fields': ['field_id'],
        'method': 'record',
    },
    # Actualización de los valores de selección de un campo de tipo de selección cuando un registro se elimina en la tabla de valores de selección de campos
    {
        'submodule': '_ddl',
        'callback': 'update_selection_values_on_delete',
        'model': 'base.model.field.selection',
        'transaction': 'delete',
        'criteria': [],
        'fields': ['field_id'],
        'method': 'record',
    },
]
