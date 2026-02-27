from ..._module_types import ValidationData

VALIDATIONS_DATA: list[ValidationData] = [

    # Genéricos
    # Restricción de creación de registros con valor de ID en creación de un registro en cualquier tabla
    {
        'module': '_validations',
        'callback': 'reject_id_values_on_create',
        'transaction': 'create',
        'method': 'record',
        'model': 'generic',
        'message': 'No se puede crear el valor de ID para el registro {data}.'
    },
    # Restricción de modificación a valores de ID en modificación de registros en cualquier tabla
    {
        'module': '_validations',
        'callback': 'reject_id_values_on_update',
        'transaction': 'update',
        'method': 'record',
        'model': 'generic',
        'message': 'No se pueden sobreescribir valores de ID en registros de la base de datos.',
    },
    # Restricción de creación de registros con valor de Fecha de creación en creación de un registro en cualquier tabla
    {
        'module': '_validations',
        'callback': 'reject_create_date_values_on_create',
        'transaction': 'create',
        'method': 'record',
        'model': 'generic',
        'message': 'No se puede crear el valor de Fecha de creación para el registro {data}.'
    },
    # Restricción de creación de registros con valor de Fecha de modificación en creación de un registro en cualquier tabla
    {
        'module': '_validations',
        'callback': 'reject_write_date_values_on_create',
        'transaction': 'create',
        'method': 'record',
        'model': 'generic',
        'message': 'No se puede crear el valor de Fecha de modificación para el registro {data}.'
    },
    # Restricción de modificación a valores de Fecha de creación en modificación de registros en cualquier tabla
    {
        'module': '_validations',
        'callback': 'reject_create_date_values_on_update',
        'transaction': 'update',
        'method': 'record',
        'model': 'generic',
        'message': 'No se pueden sobreescribir valores de Fecha de creación en registros de la base de datos.',
    },
    # Restricción de modificación a valores de Fecha de modificación en modificación de registros en cualquier tabla
    {
        'module': '_validations',
        'callback': 'reject_write_date_values_on_update',
        'transaction': 'update',
        'method': 'record',
        'model': 'generic',
        'message': 'No se pueden sobreescribir valores de Fecha de modificación en registros de la base de datos.',
    },
    # Validación de campos requeridos en creación de un registro en cualquier tabla
    {
        'module': '_validations',
        'callback': 'validate_required_fields',
        'transaction': 'create',
        'method': 'record',
        'model': 'generic',
        'message': 'Los campos {value} son requeridos en el registro {data}.',
    },
    # Restricción a valores de selección permitidos dentro de campos de tipo selección en creación de registros en cualquier tabla
    {
        'module': '_validations',
        'callback': 'validate_selection_fields_on_create',
        'transaction': 'create',
        'method': 'record',
        'model': 'generic',
        'message': 'El valor {value} no está permitido en el tipo de campo de selección.'
    },
    # Restricción a valores de selección permitidos dentro de campos de tipo selección en modificación de registros en cualquier tabla
    {
        'module': '_validations',
        'callback': 'validate_selection_fields_on_update',
        'transaction': 'update',
        'method': 'record',
        'model': 'generic',
        'message': 'El valor {value} no está permitido en el tipo de campo de selección.'
    },

    # base.model
    # Caracteres válidos en etiqueta de modelo en creación de un registro en la tabla de modelos
    {
        'module': '_validations',
        'callback': 'valid_model_label',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model',
        'message': 'El valor "{value}" en el nombre de modelo solo puede contener letras y guiones bajos.'
    },
    # Consistencia en etiqueta y modelo de nueva tabla en creación de un registro en la tabla de modelos
    {
        'module': '_validations',
        'callback': 'coherent_label_and_name_in_new_model',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model',
        'message': 'El nombre y nombre de modelo de "{value}" deben ser coincidir con el patrón "model_name" - "model.name" respectivamente.',
    },
    # Restricción de modificación de metadatos en modelos
    {
        'module': '_validations',
        'callback': 'reject_model_modification',
        'transaction': 'update',
        'method': 'record',
        'model': 'base.model',
        'message': 'Los modelos no pueden ser modificados a excepción de su nombre y descripción.',
    },
    # Restricción de eliminación de modelos base
    {
        'module': '_ddl',
        'callback': 'forbid_base_model_records_deletion',
        'transaction': 'delete',
        'method': 'record',
        'model': 'base.model',
        'message': 'No se pueden eliminar registros base.'
    },

    # base.model.field
    # Restricción de eliminación de campos base
    {
        'module': '_ddl',
        'callback': 'forbid_base_field_records_deletion',
        'transaction': 'delete',
        'method': 'record',
        'model': 'base.model.field',
        'message': 'No se pueden eliminar registros base.'
    },
    # Restricción para no modificar propiedades de un campo ya creado en modificación de un registro en la tabla de campos
    {
        'module': '_validations',
        'callback': 'unmutable_field_properties',
        'transaction': 'update',
        'method': 'record',
        'model': 'base.model.field',
        'message': 'Las propiedades de los campos que no sean la etiqueta o la información de ayuda no pueden ser modificadas en {data}. Si realmente deseas realizar modificaciones elimina el campo y vuelve a crearlo.'
    },
    # Restricción de creación de un campo en un modelo que ya tiene un campo con el mismo nombre en creación de un registro en la tabla de modelos
    {
        'module': '_validations',
        'callback': 'forbid_duplicated_fields_in_same_model',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model.field',
        'message': 'Ya existe un campo llamado "{value}" y no es posible registrar los datos {data}.'
    },
    # Restricción de ingreso de pares nombre/ID de modelo en creación de registros en la tabla de campos
    {
        'module': '_validations',
        'callback': 'forbid_duplicated_fields_in_same_model_in_incoming_data',
        'transaction': 'create',
        'method': 'list',
        'model': 'base.model.field',
        'message': 'Los pares de nombre de campo y modelo {value} no pueden existir más de una vez.'
    },
    # Restricción de etiqueta de campo duplicada en el mismo modelo en creación de un registro de campo
    {
        'module': '_validations',
        'callback': 'unique_field_label_in_model',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model.field',
        'message': 'Ya existe un campo con la etiqueta "{value}" en el modelo.'
    },
    # Restricción de etiquetas de campo repetidas en el mismo modelo en datos entrantes en creación de registros de campo.
    {
        'module': '_validations',
        'callback': 'unique_field_label_in_model_in_incomig_data',
        'transaction': 'create',
        'method': 'list',
        'model': 'base.model.field',
        'message': 'No se pueden registrar campos con la misma etiqueta en el mismo modelo. Valores de error: {value}.'
    },
    # Restricción de creación de contraseña inicial en creación de un registro en la tabla de usuarios
    {
        'module': '_validations',
        'callback': 'avoid_password_creation',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.users',
        'message': 'No se puede crear una contraseña inicial. Cambia la contraseña prestablecida una vez que el usuario [{value}] se haya creado.',
    },
    # Restricción de modificación de contraseña en la modificación de un registro en la tabla de usuarios
    {
        'module': '_validations',
        'callback': 'avoid_password_modification',
        'transaction': 'update',
        'method': 'record',
        'model': 'base.users',
        'message': 'No se puede cambiar la contraseña de un usuario por medio de la API de CRUD de Lylac.',
    },
    # Restricción de modelo relacionado en tipos de dato sencillo en creación de campos
    {
        'module': '_ddl',
        'callback': 'reject_related_model_on_single_ttype',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model.field',
        'message': 'Los tipos de dato de campo no relacionados no pueden tener modelo relacionado. El registro con error es {data}.'
    },
    # Restricción de campo relacionado en tipos de dato sencillo en creación de campos
    {
        'module': '_ddl',
        'callback': 'reject_related_field_on_single_ttype',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model.field',
        'message': 'Los tipos de dato de campo no relacionados no pueden tener campo relacionado. El registro con error es {data}.'
    },
    # Restricción de modelo relacionado nulo en tipos de dato many2one en creación de campos
    {
        'module': '_ddl',
        'callback': 'mandatory_related_model_on_many2one_ttype',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model.field',
        'message': 'Los tipos de dato de campo many2one deben contener un modelo relacionado. El registro con error es {data}.'
    },
    # Restricción de campo relacionado en tipos de dato many2one en creación de campos
    {
        'module': '_ddl',
        'callback': 'reject_related_field_on_many2one_ttype',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model.field',
        'message': 'Los tipos de dato de campo many2one no pueden tener campo relacionado. El registro con error es {data}.'
    },
    # Restricción de modelo relacionado nulo en tipos de dato one2many en creación de campos
    {
        'module': '_ddl',
        'callback': 'mandatory_related_model_on_one2many_ttype',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model.field',
        'message': 'Los tipos de dato de campo one2many deben tener modelo relacionado. El registro con error es {data}.'
    },
    # Restricción de campo relacionado nulo en tipos de dato one2many en creación de campos
    {
        'module': '_ddl',
        'callback': 'mandatory_related_field_on_one2many_ttype',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model.field',
        'message': 'Los tipos de dato de campo one2many deben tener campo relacionado. El registro con error es {data}.'
    },
    # Restricción de modelo relacionado nulo en tipos de dato many2many en creación de campos
    {
        'module': '_ddl',
        'callback': 'mandatory_related_model_on_many2many_ttype',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model.field',
        'message': 'Los tipos de dato de campo many2many deben contener un modelo relacionado. El registro con error es {data}.'
    },
    # Restricción de campo relacionado en tipos de dato many2many en creación de campos
    {
        'module': '_ddl',
        'callback': 'reject_related_field_on_many2many_ttype',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model.field',
        'message': 'Los tipos de dato de campo many2many no pueden tener campo relacionado. El registro con error es {data}.'
    },
    # Restricción para relacionar campos existentes en creación de campos one2many
    {
        'module': '_ddl',
        'callback': 'validate_related_field_existence_on_related_field',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model.field',
        'message': 'El campo al que se intenta relacionar este registro no existe. El registro con error es {data}.',
    },
    # Restricción de unicidad en combinación de modelo relacionado y campo relacionado en datos entrantes en creación de campos one2many
    {
        'module': '_ddl',
        'callback': 'unique_relation_on_one2many_in_incomig_data',
        'transaction': 'create',
        'model': 'base.model.field',
        'method': 'list',
        'message': 'Los valores {value} en modelo relacionado y campo relacionado no pueden repetirse.',
    },
    # Restricción de unicidad en combinación de modelo relacionado y campo relacionado
    {
        'module': '_ddl',
        'callback': 'unique_relation_on_one2many',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model.field',
        'message': 'No pueden existir dos campos de tipo one2many relacionados al mismo campo many2one. El registro con error es {data}.'
    },
    # Restricción de tipo de dato many2one a relacionar con campos de tipo one2many
    {
        'module': '_ddl',
        'callback': 'many2one_ttype_only_on_one2many_related_field',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model.field',
        'message': 'El tipo de dato del campo al que se intenta relacionar debe ser many2one. El registro con error es {data}.'
    },
    # Restricción de relaciones bilaterales entre el campo one2many a crear y el campo many2one a relacionar con éste
    {
        'module': '_ddl',
        'callback': 'bilateral_relationship_on_one2many_and_many2one',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model.field',
        'message': 'El modelo al que pertenece el campo relacionado debe ser el mismo al que pertenece el campo a crear. El registro con error es {data}.'
    },

    # base.model.field.selection
    # Restricción de valores de selección duplicados en la base de datos
    {
        'module': '_validations',
        'callback': 'unique_selection_value_per_field_db_validation',
        'transaction': 'create',
        'method': 'record',
        'model': 'base.model.field.selection',
        'message': 'El valor de selección [{value}] ya existe como valor de selección del campo.',
    },
    # Restricción de valores de selección duplicados en datos entrantes
    {
        'module': '_validations',
        'callback': 'unique_selection_value_per_field_data_validation',
        'transaction': 'create',
        'method': 'list',
        'model': 'base.model.field.selection',
        'message': 'No se pueden registrar valores de selección con el mismo nombre vinculados al mismo campo. Valores de error: {value}.'
    },
    # Restricción de modificación de valores de selección
    {
        'module': '_validations',
        'callback': 'reject_selection_value_modification',
        'transaction': 'update',
        'method': 'record',
        'model': 'base.model.field.selection',
        'message': 'No se pueden modificar los datos de un valor de selección. En su lugar, borra el registro completo y vuelve a crearlo.',
    },
]
