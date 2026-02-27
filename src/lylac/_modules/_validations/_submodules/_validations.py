import re
from typing import Any
from ...._constants import (
    FIELD_NAME,
    MODEL_NAME,
    ROOT_ID,
)
from ...._core.modules import Validations_Core
from ...._module_types import ModelRecordData
from .._module_types import Validation

class _Validations():
    _validations: Validations_Core

    def __init__(
        self,
        instance: Validations_Core,
    ) -> None:

        # Asignación de instancia propietaria
        self._validations = instance
        # Asignación de instancia principal
        self._main = instance._main
        # Referencia al módulo de estructura interna
        self._strc = instance._main._strc

    def reject_id_values_on_create(
        self,
        params: Validation.Create.Individual.Args,
    ) -> Any:

        # Comprobación de existencia de ID en creación
        if FIELD_NAME.ID in params.data.keys():
            return True

    def reject_id_values_on_update(
        self,
        params: Validation.Update.Individual.Args,
    ) -> Any:

        # Comprobación de existencia de ID en modificación
        if FIELD_NAME.ID in params.data.keys():
            return True

    def reject_create_date_values_on_create(
        self,
        params: Validation.Create.Individual.Args,
    ) -> Any:

        # Comprobación de existencia de Fecha de creación en creación
        if 'create_date' in params.data.keys():
            return True

    def reject_write_date_values_on_create(
        self,
        params: Validation.Create.Individual.Args,
    ) -> Any:

        # Comprobación de existencia de Fecha de modificación en creación
        if 'write_date' in params.data.keys():
            return True

    def reject_create_date_values_on_update(
        self,
        params: Validation.Update.Individual.Args,
    ) -> Any:

        # Comprobación de existencia de Fecha de creación en creación
        if 'create_date' in params.data.keys():
            return True

    def reject_write_date_values_on_update(
        self,
        params: Validation.Update.Individual.Args,
    ) -> Any:

        # Comprobación de existencia de Fecha de modificación en creación
        if 'write_date' in params.data.keys():
            return True

    def validate_selection_fields_on_create(
        self,
        params: Validation.Create.Individual.Args,
    ) -> Any:

        # Obtención de los campos de tipo selección del modelo actual
        selection_ttype_fields = self._strc.get_ttype_fields(params.model_name, 'selection')

        # Iteración por cada campo de selección encontrado
        for selection_field in selection_ttype_fields:
            # Si existe un campo de tipo selección en los datos...
            if selection_field in params.data.keys():
                # Obtención de los valores permitidos para el campo de tipo selección
                selection_values = self._strc.get_field_selection_values(params.model_name, selection_field)
                # Si el valor del campo no se encuentra dentro de los valores permitidos...
                if params.data[selection_field] not in selection_values:
                    # Se retorna el valor para generar el error
                    return params.data[selection_field]

    def validate_selection_fields_on_update(
        self,
        params: Validation.Update.Individual.Args,
    ) -> Any:

        # Obtención de los campos de tipo selección del modelo actual
        selection_ttype_fields = self._strc.get_ttype_fields(params.model_name, 'selection')

        # Iteración por cada campo de selección encontrado
        for selection_field in selection_ttype_fields:
            # Si existe un campo de tipo selección en los datos...
            if selection_field in params.data.keys():
                # Obtención de los valores permitidos para el campo de tipo selección
                selection_values = self._strc.get_field_selection_values(params.model_name, selection_field)
                # Si el valor del campo no se encuentra dentro de los valores permitidos...
                if params.data[selection_field] not in selection_values:
                    # Se retorna el valor para generar el error
                    return params.data[selection_field]

    def reject_model_modification(
        self,
        params: Validation.Update.Individual.Args[ModelRecordData.BaseModel_],
    ) -> Any:

        # Revisión de los valores que se intentan escribir en el modelo
        for field in params.data.keys():
            if field not in ['label', 'decription']:
                return True

    def validate_required_fields(
        self,
        params: Validation.Create.Individual.Args[ModelRecordData.BaseModelField],
    ) -> Any:
        """
        ### Validación de campos requeridos
        Esta validación revisa en la base de datos cuáles son los campos requeridos en
        el modelo de la transacción, revisa los datos entrantes y valida que el
        diccionario entrante contenga las llaves de los campos requeridos. Arroja un
        error si encuentra una llave faltante.
        """

        # Obtención de los campos requeridos
        required_fields: list[str] = (
            self._main.search_read(
                ROOT_ID,
                MODEL_NAME.BASE_MODEL_FIELD,
                [
                    '&',
                        ('model_id', '=', params.model_id),
                        ('is_required', '=', True)
                ],
                ['name'],
                output_format= 'dataframe',
            )
            ['name']
            .to_list()
        )

        # Inicialización de lista de campos faltantes
        missing_fields: list[str] = []

        # Iteración por cada campo requerido
        for required_field in required_fields:
            # Si el campo requerido no está en los datos entrantes de creación...
            if required_field not in params.data.keys():
                # Se añade el nombre del campo a los campos faltantes
                missing_fields.append(required_field)

        # Si existen campos faltantes
        if missing_fields:
            # Se retorna la información
            return missing_fields

    def coherent_label_and_name_in_new_model(
        self,
        params: Validation.Create.Individual.Args[ModelRecordData.BaseModel_],
    ) -> Any:
        """
        ### Coherencia en nombre y etiqueta de modelo
        Esta validación compara la etiqueta del nuevo modelo y se asegura que el nombre
        modelo cumpla con la estructura de reemplazo de guiones bajos por puntos.

        Ejemplo:

        `base_permissions` - `base.permissions`

        Arroja un error si el formato no coincide.
        """

        # Obtención del nombre del modelo a crear
        record_name = params.data['name']
        # Obtención del nombre de modelo del modelo a crear
        record_model = params.data['model']

        # Comparación
        if record_name.replace('_', '.') != record_model:
            return record_model

    def valid_model_label(
        self,
        params: Validation.Create.Individual.Args[ModelRecordData.BaseModel_],
    ) -> Any:
        """
        ### Etiqueta de modulo válida
        Esta validación se asegura que la etiqueta del nuevo modelo solo contenga
        letras minúsculas y guiones bajos en ésta.
        """

        # Obtención del nombre del modelo
        model_name = params.data['name']

        # Se valida que el nombre con los caracteres válidos
        coincidence = re.match(r'^[a-z_]*$', model_name)

        # Si no existe coincidencia se retorna el nombre
        if coincidence is None:
            return model_name

    def unmutable_field_properties(
        self,
        params: Validation.Update.Individual.Args[ModelRecordData.BaseModelField],
    ) -> Any:
        """
        ### Propiedades de campo inmutables
        Esta validación se asegura de que solo la etiqueta de campo sea editable ya que
        no es posible realizar modificaciones de propiedades a columnas de tablas en la
        base de datos.
        """

        # Campos válidos
        valid_fields = ['label', 'help_info']

        # Revisión
        for field in params.data.keys():
            # Si se encuentra un campo que no es válido...
            if field not in valid_fields:
                # Se retorna True para disparar el error
                return True

    def forbid_duplicated_fields_in_same_model(
        self,
        params: Validation.Create.Individual.Args[ModelRecordData.BaseModelField],
    ) -> Any:
        """
        ### Prohibir campos duplicados en modelo
        Esta validación se asegura que cada diccionario de datos entrante para la
        creación de un nuevo registro en el campo de modelos no incluya un nombre de
        campo combinado con una ID de modelo vinculada que ya exista en la base de
        datos. Arroja un error si encuentra coincidencias.
        """

        # Obtención de los valores a usar en filtro
        field_name = params.data['name']
        model_id = params.data['model_id']

        # Búsqueda de coincidencias
        records = self._main.search_read(
            ROOT_ID,
            'base.model.field',
            [
                '&',
                    ('name', '=', field_name),
                    ('model_id', '=', model_id)
            ],
            ['name', 'model_id'],
            output_format= 'dataframe',
            only_ids_in_relations= True,
        )

        # Si existen coincidencias se retorna el nombre del campo
        if len(records):
            return field_name

    def forbid_duplicated_fields_in_same_model_in_incoming_data(
        self,
        params: Validation.Create.Group.Args[ModelRecordData.BaseModelField],
    ) -> Any:
        """
        Prohibir campos duplicados en modelo desde datos entrantes
        Esta validación se asegura que cada diccionario de datos entrante para la
        creación de un nuevo registro en el campo de modelos no incluya un nombre de
        campo combinado con una ID de modelo vinculada dos veces en los datos entrantes.
        """

        # Obtención de cantidad de registros a crear
        incoming_records_qty = len(params.data)

        # Si solo existe un registro la función se termina ya que no hay suficientes datos a comparar
        if incoming_records_qty == 1:
            return None

        # Obtención de lista de duplicados
        duplicated_pairs = self._main._algorythms.find_duplicates(
            params.data,
            lambda value: ( value['name'], value['model_id'] ),
        )

        # Si existen pares duplicados se retornan éstos
        if len(duplicated_pairs):
            return duplicated_pairs

    def unique_field_label_in_model(
        self,
        params: Validation.Create.Individual.Args[ModelRecordData.BaseModelField],
    ) -> Any:
        """
        ### Etiqueta de campo única por modelo
        Esta validación se asegura que los datos entrantes no contengan una etiqueta de
        campo ya existente en el modelo en donde se intenta crear el registro. Arroja
        un error en caso de hallar un registro de campo con la misma etiqueta de los
        datos entrantes.
        """

        # Obtención de los valores a usar en el filtro
        field_label = params.data['label']
        model_id = params.data['model_id']

        # Búsqueda de coincidencias
        results = self._main.search_read(
            ROOT_ID,
            'base.model.field',
            [
                '&',
                    ('label', '=', field_label),
                    ('model_id', '=', model_id)
            ]
        )

        # Si existen coincidencias se retona el nombre del campo y la ID de modelo
        if len(results):
            return field_label

    def unique_field_label_in_model_in_incomig_data(
        self,
        params: Validation.Create.Group.Args[ModelRecordData.BaseModelField],
    ) -> Any:
        """
        ### Etiqueta de campo única por modelo en datos entrantes
        Esta validación se asegura que los datos entrantes no contengan una etiqueta de
        campo repetida en los datos entrantes. Arroja un error en caso de hallar
        valores en etiqueta de campo repetidos en los datos entrantes.
        """

        # Búsqueda de duplicados
        duplicated = self._main._algorythms.find_duplicates(
            params.data,
            lambda record: ( record['label'], record['model_id'] ),
        )

        # Si existen nombres duplicados se retornan éstos
        if len(duplicated):
            return duplicated

    def unique_selection_value_per_field_db_validation(
        self,
        params: Validation.Create.Individual.Args[ModelRecordData.BaseModelFieldSelection],
    ) -> Any:

        # Búsqueda de resultados
        results_qty = self._main.search_count(
            ROOT_ID,
            MODEL_NAME.BASE_MODEL_FIELD_SELECTION,
            [
                '&',
                    ('name', '=', params.data['name']),
                    ('field_id', '=', params.data['field_id']),
            ],
        )

        # Si existe algún registro...
        if results_qty:
            # Se retorna el nombre del valor repetido
            return ( params.data['name'] )

    def unique_selection_value_per_field_data_validation(
        self,
        params: Validation.Create.Group.Args[ModelRecordData.BaseModelFieldSelection],
    ) -> Any:

        # Búsqueda de valores duplicados
        duplicated_values = self._main._algorythms.find_duplicates(
            params.data,
            lambda value: ( value['name'], value['field_id'] )
        )

        # Si existen valores duplicados en los datos entrantes
        if len(duplicated_values):
            return duplicated_values

    def reject_selection_value_modification(
        self,
        params: Validation.Update.Individual.Args[ModelRecordData.BaseModelFieldSelection],
    ) -> Any:

        # Iteración por cada campo que se intenta modificar en el registro
        for field in params.data.keys():
            # Si el campo no existe en los valores permitidos...
            if field not in ['label']:
                # Se genera el error
                return True

    def avoid_password_creation(
        self,
        params: Validation.Create.Individual.Args[ModelRecordData.BaseUsers],
    ) -> Any:
        """
        ### Restricción de contraseña inicial
        Esta validación se asegura que no se ingrese una contraseña sin ser hasheada.
        """

        # Comprobación de existencia de Contraseña en datos entrantes
        if 'password' in params.data.keys():
            return params.data['name']

    def avoid_password_modification(
        self,
        params: Validation.Update.Individual.Args[ModelRecordData.BaseUsers],
    ) -> Any:

        # Comprobación de existencia de Contraseña en datos entrantes
        if 'password' in params.data.keys():
            return params.data['name']
