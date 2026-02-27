from ..._contexts._computed import _ComputeContextCore

def _base_model__display_name(
    ctx: _ComputeContextCore,
):

    # Obtención de la etiqueta del modelo
    label = ctx['label']
    # Obtención del nombre de modelo
    model = ctx['model']
    # Creación del nombre
    field = label + ' (' + model + ')'

    return field

def _base_model_field__display_name(
    ctx: _ComputeContextCore,
):

    # Obtención del nombre de modelo del modelo del campo
    model_model_name = ctx['model_id.model']
    # Obtención de la etiqueta del campo
    label = ctx['label']
    # Creación del nombre visible
    field = label + ' (' + model_model_name + ')'

    return field

def _base_model_field_selection__display_name(
    ctx: _ComputeContextCore,
):

    # Obtención de la etiqueta del registro
    label = ctx['label']
    # Obtención del nombre visible del campo
    field_display_name = ctx['field_id.display_name']
    # Creación del nombre visible del valor de selección
    field = ctx.concat(label, '|', field_display_name, sep= ' ')

    return field

def _base_model_access_groups__display_name(
    ctx: _ComputeContextCore,
):

    # Obtención de la etiqueta del grupo
    field = ctx['label']

    return field

class COMPUTED_FIELD:

    class BASE_MODEL:
        display_name = _base_model__display_name

    class BASE_MODEL_FIELD:
        display_name = _base_model_field__display_name

    class BASE_MODEL_FIELD_SELECTION:
        display_name = _base_model_field_selection__display_name

    class BASE_MODEL_ACCESS_GROUPS:
        display_name = _base_model_access_groups__display_name
