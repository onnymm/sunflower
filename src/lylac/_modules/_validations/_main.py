from ..._constants import (
    MODEL_NAME,
    ROOT_ID,
)
from ..._core.main import _Lylac_Core
from ..._core.modules import Validations_Core
from ..._module_types import (
    CriteriaStructure,
    RecordData,
    ModelName,
    WriteTransactionName,
)
from ._module_types import (
    ErrorToShow,
    Validation,
    ValidationsHub,
)
from ._submodules import (
    _Automations,
    _Initialize,
    _Validations,
)

class Validations(Validations_Core):

    _hub: ValidationsHub = {}
    _active: bool = False

    def __init__(
        self,
        instance: _Lylac_Core,
    ) -> None:

        # Asignación de instancia principal
        self._main = instance
        # Asignación de instancia de estructura interna
        self._strc = instance._strc

        # Inicialización de submódulos
        self._m_automations = _Automations(self)
        self._m_initialize = _Initialize(self)
        self._m_validations = _Validations(self)

    def initialize(
        self,
    ) -> None:

        # Inicialización de los datos
        self._m_initialize.initialize_data()
        # Se activa el estado de las validaciones para comenzar a funcionar
        self._active = True

    def initialize_model_validations(
        self,
        model_name: ModelName,
    ) -> None:

        self._hub[model_name] = {
            'create': [],
            'update': [],
            'delete': [],
        }

    def drop_model_validations(
        self,
        model_name: ModelName,
    ) -> None:

        del self._hub[model_name]

    def run_validations_on_create(
        self,
        model_name: ModelName,
        data: list[RecordData],
    ) -> None:

        # Si el estado de las automatizaciones aún no es activo
        if not self._active:
            return

        # Obtención de la ID del modelo
        [ model_id ] = self._main.search(ROOT_ID, MODEL_NAME.BASE_MODEL, [('model', '=', model_name)])

        # Obtención de las validaciones del modelo en el método de creación
        transaction_validations: list[Validation.Create.Mixed.Params] = self._get_method_validations(model_name, 'create')

        # Iteración por cada una de las validaciones
        for validation in transaction_validations:

            # Inicialización de errores
            errors: list[ErrorToShow] = []

            # Si la validación se debe ejecutar por registro...
            if validation['method'] == 'record':

                # Obtención de la función de validación a ejecutar
                validation_to_execute: Validation.Create.Individual.Callback = validation['callback']
                # Iteración por cada uno de los registros
                for record in data:
                    # Ejecución de validación y obtención de posible valor a mostrar en error
                    error_value = validation_to_execute(
                        Validation.Create.Individual.Args(
                            model_name= model_name,
                            model_id= model_id,
                            data= record,
                        ),
                    )

                    # Si existe valor retornado
                    if error_value is not None:
                        # Se añaden datos de error
                        errors.append(
                            {
                                'value': error_value,
                                'message': validation['message'],
                                'data': record
                            }
                        )

            # Si la validación se debe ejecutar por grupo de registros...
            else:

                # Obtención de la función de validación a ejecutar
                validation_to_execute: Validation.Create.Group.Callback = validation['callback']
                # Se ejecuta la función con todos los registros
                error_value = validation_to_execute(
                    Validation.Create.Group.Args(
                        model_name= model_name,
                        model_id= model_id,
                        data = data,
                    )
                )

                # Si existe valor retornado
                if error_value is not None:
                    # Se añaden datos de error
                    errors.append(
                        {
                            'value': error_value,
                            'message': validation['message'],
                            'data': data,
                        }
                    )

            # Si existen errores encontrados
            if errors:
                # Inicialización de mensaje completo
                complete_message = '\n'
                for err in errors:
                    message = err['message'].format(value= err['value'], data= err['data'])
                    complete_message += f'{message}\n'

                # Se arrojan el error
                raise AssertionError(complete_message)

    def run_validations_on_delete(
        self,
        model_name: ModelName,
        record_ids: list[int],
    ) -> None:

        # Si el estado de las automatizaciones aún no es activo
        if not self._active:
            return

        # Obtención de la ID del modelo
        [ model_id ] = self._main.search(ROOT_ID, MODEL_NAME.BASE_MODEL, [('model', '=', model_name)])
        # Obtención de los datos de los registros
        records_data = self._main.read(ROOT_ID, model_name, record_ids, output_format= 'dict')
        # Obtención de las validaciones del modelo en el método de eliminación
        transaction_validations: list[Validation.Create.Mixed.Params] = self._get_method_validations(model_name, 'delete')

        # Iteración por cada una de las validaciones
        for validation in transaction_validations:

            # Inicialización de errores
            errors: list[ErrorToShow] = []

            # Si la validación se debe ejecutar por registro...
            if validation['method'] == 'record':

                # Obtención de la función de validación a ejecutar
                validation_to_execute: Validation.Create.Individual.Callback = validation['callback']
                # Iteración por cada uno de los registros
                for record in records_data:
                    # Creación de los datos a proporcionar a la función
                    data = Validation.Create.Individual.Args(
                        model_name= model_name,
                        model_id= model_id,
                        data= record,
                    )
                    # Ejecución de validación y obtención de posible valor a mostrar en error
                    error_value = validation_to_execute(data)

                    # Si existe valor retornado
                    if error_value is not None:
                        # Se añaden datos de error
                        errors.append(
                            {
                                'value': error_value,
                                'message': validation['message'],
                                'data': record
                            }
                        )

            # Si la validación se debe ejecutar por grupo de registros...
            else:

                # Obtención de la función validación a ejecutar
                validation_to_execute: Validation.Create.Group.Callback = validation['callback']
                # Creación de los datos a proporcionar a la función
                data = Validation.Create.Individual.Args(
                    model_name= model_name,
                    model_id= model_id,
                    data= records_data,
                )

                # Se ejecuta la función con todos los registros
                error_value = validation_to_execute(data)

                # Si existe valor retornado
                if error_value is not None:
                    # Se añaden datos de error
                    errors.append(
                        {
                            'value': error_value,
                            'message': validation['message'],
                            'data': data,
                        }
                    )

            # Si existen errores encontrados
            if errors:
                # Inicialización de mensaje completo
                complete_message = '\n'
                for err in errors:
                    message = err['message'].format(value= err['value'], data= err['data'])
                    complete_message += f'{message}\n'

                # Se arrojan el error
                raise AssertionError(complete_message)

    def run_validations_on_update(
        self,
        model_name: ModelName,
        search_criteria: CriteriaStructure,
        data: RecordData,
    ) -> None:

        # Si el estado de las automatizaciones aún no es activo
        if not self._active:
            return

        # Obtención de la ID del modelo
        [ model_id ] = self._main.search(ROOT_ID, MODEL_NAME.BASE_MODEL, [('model', '=', model_name)])

        # Obtención de las IDs de registros
        record_ids = self._main.search(ROOT_ID, MODEL_NAME.BASE_MODEL, search_criteria)

        # Obtención de las validaciones del modelo en el método de modificación
        transaction_validations: list[Validation.Update.Mixed.Params] = self._get_method_validations(model_name, 'update')

        # Inicialización de errores
        errors: list[ErrorToShow] = []

        # Iteración por cada una de las validaciones
        for validation in transaction_validations:

            # Si la validación se debe ejecutar por registro...
            if validation['method'] == 'record':

                # Obtención de la función de validación a ejecutar
                validation_to_execute: Validation.Update.Individual.Callback = validation['callback']
                # Iteración por cada uno de los registros
                for record_id in record_ids:
                    # Ejecución de validación y obtención de posible valor a mostrar en error
                    error_value = validation_to_execute(
                        Validation.Update.Individual.Args(
                            model_name= model_name,
                            model_id= model_id,
                            record_ids= record_id,
                            data= data,
                        )
                    )

                    # Si existe valor retornado
                    if error_value is not None:
                        # Se añaden datos de error
                        errors.append(
                            {
                                'value': error_value,
                                'message': validation['message'],
                                'data': record_id,
                            }
                        )

            # Si la validacións e debe ejecutar por grupo de registros...
            else:

                # Obtención de la función de validación a ejecutar
                validation_to_execute: Validation.Update.Group.Callback = validation['callback']
                # Se ejecuta la función con todos los registros
                error_value = validation_to_execute(
                    Validation.Update.Group.Args(
                        model_name= model_name,
                        model_id= model_id,
                        record_ids= record_ids,
                        data= data,
                    )
                )

                # Si existe valor retornado
                if error_value is not None:
                    # Se añaden datos de error
                    errors.append(
                        {
                            'value': error_value,
                            'message': validation['message'],
                            'data': data,
                        }
                    )

        # Si existen errores encontrados
        if errors:
            # Iniciailización de mensaje completo
            complete_message = '\n'
            for err in errors:
                message = err['message'].format(value= err['value'], data= err['data'])
                complete_message += f'{message}\n'

            # Se arroja el error
            raise AssertionError(complete_message)

    def _get_method_validations(
        self,
        model_name: ModelName,
        transaction: WriteTransactionName,
    ):

        # Obtención de validaciones genéricas
        generic_validations = self._hub['generic'][transaction]
        # Obtención de validaciones del modelo
        model_validations = self._hub[model_name][transaction]

        # Creación de lista de validaciones
        validations = [ *generic_validations, *model_validations ]

        return validations
