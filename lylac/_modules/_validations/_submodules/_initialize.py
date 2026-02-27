from ...._data import (
    INITIAL_DATA,
    VALIDATIONS_DATA,
)
from ...._core.modules import Validations_Core
from ...._core.submods.validations import _Initialize_Interface

class _Initialize(_Initialize_Interface):
    _validations: Validations_Core

    def __init__(
        self,
        instance: Validations_Core,
    ) -> None:

        # Asignación de instancia propietaria
        self._validations = instance
        # Asignación de instancia principal
        self._main = instance._main
        # Generación de nombres de modelos iniciales
        self._initial_models = [ model for ( model, _ ) in INITIAL_DATA ] + ['base.users']

    def initialize_data(
        self,
    ) -> None:

        # Genéricos
        self._validations.initialize_model_validations('generic')

        # Modelos iniciales
        for model_name in self._initial_models:
            self._validations.initialize_model_validations(model_name)

        for validation_data in VALIDATIONS_DATA:
            # Si no fue definido un modelo específico para la validación
            if validation_data['model'] is None:
                # Se define la validación para todos los modelos
                model = 'generic'
            else:
                # Se define la validación para el modelo especificado
                model = validation_data['model']

            # Obtención del nombre de la transacción para la que aplica la validación
            transaction = validation_data['transaction']

            # Obtención de la función de validación
            validation_callback = self._get_validation_callback(validation_data['module'], validation_data['callback'])

            # Se guarda la validación y sus parámetros en el núcleo de validaciones
            self._validations._hub[model][transaction].append(
                {
                    'callback': validation_callback,
                    'message': validation_data['message'],
                    'method': validation_data['method'],
                }
            )

    def _get_validation_callback(
        self,
        module_name: str,
        callback_name: str,
    ):

        # Obtención del módulo de la instancia principal
        module_extension = getattr(self._main, module_name)
        # Obtención del submódulo de validaciones del módulo de la instancia
        validations_submodule = getattr(module_extension, '_m_validations')
        # Obtención de la referencia de la función de validación
        validation_callback = getattr(validations_submodule, callback_name)

        return validation_callback
