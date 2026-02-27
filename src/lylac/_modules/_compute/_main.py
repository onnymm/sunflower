from ..._constants import (
    FIELD_NAME,
    MODEL_NAME,
)
from ..._core.main import _Lylac_Core
from ..._core.modules import Compute_Core
from ..._data import COMPUTED_FIELD
from ..._module_types import (
    ComputedFieldCallback,
    ModelName,
    TTypeName,
)
from ._submodules import _Automations

class Compute(Compute_Core):

    hub = dict[ModelName, dict[str, ComputedFieldCallback]]

    def __init__(
        self,
        instance: _Lylac_Core,
    ) -> None:

        # Asignación de instancia principal
        self._main = instance
        # Inicialización de submódulo de automatizaciones
        self._m_automations = _Automations(self)

        # Inicialización del módulo
        self._initialize()

    def _initialize(
        self,
    ) -> None:

        # Obtención de los nombres de los modelos
        models = self._main._strc.get_model_names()
        # Inicialización del núcleo de campos computados
        self.hub = { model: {} for model in models }

    def initialize_default_computed_fields(self):

        # Se realiza el registro de las funciones de cálculo
        self.hub[MODEL_NAME.BASE_MODEL][FIELD_NAME.DISPLAY_NAME] = COMPUTED_FIELD.BASE_MODEL.display_name
        self.hub[MODEL_NAME.BASE_MODEL_FIELD][FIELD_NAME.DISPLAY_NAME] = COMPUTED_FIELD.BASE_MODEL_FIELD.display_name
        self.hub[MODEL_NAME.BASE_MODEL_FIELD_SELECTION][FIELD_NAME.DISPLAY_NAME] = COMPUTED_FIELD.BASE_MODEL_FIELD_SELECTION.display_name
        self.hub[MODEL_NAME.BASE_MODEL_ACCESS_GROUPS][FIELD_NAME.DISPLAY_NAME] = COMPUTED_FIELD.BASE_MODEL_ACCESS_GROUPS.display_name

    def register_computed_field(
        self,
        model_name: ModelName,
        ttype: TTypeName,
        field_name: str,
        field_label: str,
        compute_field_callback: ComputedFieldCallback,
    ) -> None:

        # Búsqueda del registro del modelo
        [ record ] = self._main.search_read(
            self._main._ROOT_USER,
            MODEL_NAME.BASE_MODEL,
            [('model', '=', model_name)],
            output_format= 'dict',
        )
        # Obtención de la ID del modelo
        model_id = record[FIELD_NAME.ID]

        # Búsqueda de algún campo computado existente
        found_ids = self._main.search(
            self._main._ROOT_USER,
            MODEL_NAME.BASE_MODEL_FIELD,
            [
                '&',
                    ('name', '=', field_name),
                    '&',
                        ('model_id', '=', model_id),
                        '&',
                            ('ttype', '=', ttype),
                            ('is_computed', '=', True),
            ]
        )

        # Si no se encontraron coincidencias...
        if not found_ids:
            # Se crea el registro en la base de datos
            [ created_field_id ] = self._main.create(
                self._main._ROOT_USER,
                MODEL_NAME.BASE_MODEL_FIELD,
                {
                    'name': field_name,
                    'label': field_label,
                    'ttype': ttype,
                    'model_id': model_id,
                    'is_computed': True,
                },
            )

            # Obtención de posibles valores de selección
            selection_values = (
                self._main.search_read(
                    self._main._ROOT_USER,
                    MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
                    [('field_id', '=', created_field_id)],
                    [FIELD_NAME.NAME],
                    output_format= 'dataframe',
                )
                [FIELD_NAME.NAME]
                .to_list()
            )

        # Si existen coincidencias...
        else:
            # Se inicializa la variable como lista vacía
            selection_values = []

        # Registro de la función
        self._register_field_computation(model_name, field_name, compute_field_callback)
        # Registro de campo en la estructura
        self._main._strc.register_field(model_name, field_name, ttype, None, None, selection_values, True)

    def _register_field_computation(
        self,
        model_name: ModelName,
        field_name: str,
        computation_callback: ComputedFieldCallback,
    ) -> None:

        # Registro de la función en el núcleo
        self.hub[model_name][field_name] = computation_callback

    def register_model(
        self,
        model_name: ModelName,
    ) -> None:

        # Registro del modelo como un diccionario vacío
        self.hub[model_name] = {}

    def unregister_model(
        self,
        model_name: ModelName,
    ) -> None:

        # Se elimina el diccionario del modelo
        del self.hub[model_name]
