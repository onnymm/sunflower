from sqlalchemy.exc import ProgrammingError
from ...._constants import (
    MESSAGES,
    MODEL_NAME,
    ROOT_ID,
)
from ...._core import ENV_VARIABLES
from ...._data import (
    BASE_USERS_INITIAL_DATA,
    INITIAL_DATA,
)
from ....security import hash_password
from ....errors import InitializationError
from ...._core.modules import DDL_Core
from ...._core.submods.ddl import _Reset_Interface

class _Reset(_Reset_Interface):
    _ddl: DDL_Core

    def __init__(
        self,
        instance: DDL_Core,
    ) -> None:

        # Se inicializa estado de inicialización en falso
        self._state = False
        # Asignación de instancia propietaria
        self._ddl = instance
        # Asignación de instancia principal
        self._main = instance._main
        # Asignación del motor de conexión
        self._engine = instance._main._engine
        # Asignación de modelos iniciales
        self._base_models = [ model for ( model, _ ) in INITIAL_DATA ] + [MODEL_NAME.BASE_USERS]

    def initialize_from_data(
        self,
    ) -> None:

        # Se realiza un intento por leer datos en la base de datos
        try:
            self._main.search(ROOT_ID, MODEL_NAME.BASE_MODEL)
            # Si existen datos se construye la estructura de modelos a partir de los datos
            self._build_instance_structure()
        # Si no existen los datos se realiza una inicialización desde cero
        except ProgrammingError as _:
            self._initialize()

        # Inicialización de atributos de los campos de los modelos
        self._main._strc.initialize_fields_atts()

        # Inicialización del módulo de manejo de accesos
        self._main._access.initialize()

    def _build_instance_structure(
        self,
    ) -> None:

        # Inicialización de modelos
        self._build_models_structure()
        # Inicialización de campos
        self._build_fields_structure()
        # Inicialización de tablas de relación
        self._build_relation_models_structure()

    def _build_models_structure(
        self,
    ) -> None:

        # Lectura de todos los registros de modelos existentes
        model_records = self._main.search_read(
            ROOT_ID,
            MODEL_NAME.BASE_MODEL,
            [('state', '!=', 'base')],
            ['model', 'name'],
            output_format= 'dict'
        )

        for record in model_records:
            # Creación de los modelos de SQLAlchemy en la instancia
            self._ddl._m_model.create_model(record['name'])
            # Inicialización de diccionarios de automatizaciones
            self._main._automations.register_model(record['model'])
            # Inicialización de diccionarios de validaciones
            self._main._validations.initialize_model_validations(record['model'])
            # Inicialización de diccionarios de campos computados
            self._main._compute.register_model(record['model'])
            # Inicialización de diccionarios de acciones
            self._main._actions.register_model(record['model'])

    def _build_fields_structure(
        self,
    ) -> None:

        # Lectura de todos los registros de campos existentes
        field_records = self._main.search_read(
            ROOT_ID,
            MODEL_NAME.BASE_MODEL_FIELD,
            [
                '&',
                    '&',
                        ('state', '!=', 'base'),
                        ('name', 'not in', ['id', 'name', 'create_date', 'write_date']),
                    ('ttype', '!=', 'many2many'),
            ],
            [
                'name',
                'model_id',
                'label',
                'ttype',
                'nullable',
                'is_required',
                'unique',
                'help_info',
                'related_model_id',
                'default_value',
                'is_computed',
            ],
            output_format= 'dict',
            only_ids_in_relations= True,
        )

        # Creación de las instancias de columna en los modelos de SQLAlchemy de la instancia
        for record in field_records:
            # Obtención del nombre del modelo al que el campo pertenece
            model_name = self._main.get_value(ROOT_ID, MODEL_NAME.BASE_MODEL, record['model_id'], 'model')
            # Obtención del modelo SQLAlchemy de la instancia
            model_model = self._main._models.get_model_model(model_name)
            # Creación del objeto de atributos de campo
            field_atts = self._ddl._m_model.build_field_atts(record)
            # Si el campo no es one2many...
            if field_atts.ttype != 'one2many' and field_atts.is_computed == False:
                # Adición del campo al modelo SQLAlchemy
                self._ddl._m_model.add_field_to_model(model_model, field_atts)

        # Se establece el estado de inicialización a verdadero
        self._state = True

    def _build_relation_models_structure(
        self,
    ) -> None:

        field_records = self._main.search_read(
            ROOT_ID,
            MODEL_NAME.BASE_MODEL_FIELD,
            [('ttype', '=', 'many2many')],
            [
                'model_id.model',
                'related_model_id.model',
            ],
            output_format= 'dict',
            only_ids_in_relations= True,
        )

        for record in field_records:
            # Obtención del nombre del modelo al que el campo pertenece
            model_name = record['model_id.model']
            # Obtención del nombre del modelo al que el campo se relaciona
            related_model_name = record['related_model_id.model']
            # Creación del modelo SQLAlchemy
            self._ddl._m_model.create_relation(model_name, related_model_name)

    def _initialize(
        self
    ) -> None:
        """
        ### Inicialización de base de datos
        Este método está diseñado para ser ejecutado una única vez en todo el ciclo de
        vida de la base de datos. Permite inicializar la estructura inicial de la base
        de datos para comenzar a trabajar con ella. Este método arrojará error tras 
        intentar ser ejecutado si existen datos en la base de datos.
        """

        # Si la base de datos ya está inicializada se aborta la operación
        if self._state:
            raise InitializationError(MESSAGES.RESET.ALREADY_INITIALIZED)

        # Inicialización de la base de datos
        self._main._base.metadata.create_all(self._engine)
        # Registro del usuario inicial
        self._main.create(ROOT_ID, MODEL_NAME.BASE_USERS, BASE_USERS_INITIAL_DATA)
        # Registro de los datos iniciales
        for ( model_name, data ) in INITIAL_DATA:
            self._main.create(ROOT_ID, model_name, data)

        # Se añaden los campos 'create_uid' y'write_uid'
        # self._add_uid_columns()

        # Se escribe usuario de creación y modificación en todos los registros existentes
        for model_name in self._base_models:
            self._main.update_where(ROOT_ID, model_name, [], {'create_uid': 1, 'write_uid': 1})

        # Creación del usuario administrador
        self._create_admin_user()

        # Implementación de roles de usuario
        self._main.update(
            ROOT_ID,
            MODEL_NAME.BASE_USERS,
            [1, 2],
            {
                'role_ids': [ ('add', [1]) ],
            }
        )

        # Se cambia el estado de inicialización a verdadero
        self._state = True

    def _drop_all(
        self
    ):
        """
        ### Eliminación de la base de datos
        ⚠️ Este método elimina todos los datos y tablas de la base de datos.
        """

        # Eliminación de todos los datos
        self._main._base.metadata.drop_all(self._engine)
        # Se reinicia el estado de inicialización
        self._state = False

    def _add_uid_columns(
        self
    ) -> None:
        """
        ### Creación de columnas de registro uid
        Este método interno ejecuta la creación de las columnas `create_uid` y
        `write_uid` en cada uno de los modelos registrados inicialmente en la base de
        datos.
        """

        # Obtención de las IDs de los modelos iniciales que existen registrados en la base de datos
        model_ids = self._main.search(ROOT_ID, MODEL_NAME.BASE_MODEL)

        # Creación de las columnas por cada modelo
        for model_id in model_ids:
            self._ddl.add_default_to_model(model_id)

    def _create_admin_user(
        self,
    ) -> None:

        self._main.create(
            ROOT_ID,
            MODEL_NAME.BASE_USERS,
            {
                'name': ENV_VARIABLES.ADMIN_USER.NAME,
                'login': ENV_VARIABLES.ADMIN_USER.LOGIN,
                'password': hash_password(ENV_VARIABLES.ADMIN_USER.PASSWORD),
            }
        )
