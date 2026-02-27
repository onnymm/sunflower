from typing import (
    Callable,
    Generic,
    Union,
)
import pandas as pd
from ._constants import (
    FIELD_NAME,
    FIELD_LABEL,
    MODEL_NAME,
)
from ._contexts import AutomationContext
from ._contexts._actions import ActionCallback
from ._core.main import _Lylac_Core
from ._module_types import (
    _M,
    CriteriaStructure,
    RecordData,
    CredentialsAlike,
    DynamicModelField,
    ExecutionMethod,
    ModelName,
    OutputOptions,
    RecordValue,
    TTypeName,
    WriteTransactionName,
)
from ._modules import (
    Access,
    Actions,
    Algorythms,
    Auth,
    Automations,
    Compute,
    Compiler,
    Connection,
    DDLManager,
    DMLManager,
    DQLManager,
    Index,
    Metadata,
    Models,
    Output,
    Preprocess,
    Select,
    Structure,
    Subtransaction,
    Query,
    Validations,
    Where,
)
from .errors import IlegalComputedFieldRegistration

class Lylac(_Lylac_Core, Generic[_M]):

    def __init__(
        self,
        credentials: CredentialsAlike = None,
        output_format: OutputOptions | None = None,
    ) -> None:

        # Asignación del modelo base
        self._metadata = Metadata(self)
        # Inicialización del módulo de manejo de formato de salida
        self._output = Output(self, output_format)
        # Creación de la instancia de conexión con la base de datos
        self._connection = Connection(self, credentials)

        # Inicialización de submódulos
        self._algorythms = Algorythms(self)
        self._strc = Structure(self)
        self._models = Models(self)
        self._index = Index(self)
        self._select = Select(self)
        self._query = Query(self)
        self._where = Where(self)
        self._compiler = Compiler(self)
        self._ddl = DDLManager(self)
        self._dml = DMLManager(self)
        self._dql = DQLManager(self)
        self._auth = Auth(self)
        self._access = Access(self)
        self._preprocess = Preprocess(self)
        self._automations = Automations(self)
        self._validations = Validations(self)
        self._subtransaction = Subtransaction(self)
        self._actions = Actions(self)
        self._compute = Compute(self)

        # Registro de las automatizaciones predeterminadas
        self._automations.create_preset_automations()
        # Inicialización de estructura de modelos de la instancia
        self._ddl._m_reset.initialize_from_data()
        # Inicialización de funciones predeterminadas de campos computados
        self._compute.initialize_default_computed_fields()
        # Inicialización de los datos de validaciones
        self._validations.initialize()

    def login(
        self,
        login: str,
        password: str,
    ) -> str | bool:

        return self._auth.login(login, password)

    def authenticate(
        self,
        token: str,
    ) -> int:

        # Obtención de la ID del usuario
        user_id = self._auth.identify_user(token)

        return user_id

    def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str,
        close_sessions: bool = True,
    ) -> None:

        # Intento de cambio de contraseña
        self._auth.change_password(
            user_id,
            old_password,
            new_password,
            close_sessions,
        )

    def reset_password(
        self,
        user_id: int,
        user_id_to_reset_password: int,
    ) -> bool:

        # Validación de permiso de transacción
        self._access.check_permission(
            user_id,
            MODEL_NAME.BASE_USERS,
            'update',
        )

        # Se restablece la contraseña del usuario especificado
        self._auth.reset_password(user_id_to_reset_password)

        return True

    def assign_display_name(
        self,
        model_name: Union[ModelName, _M],
    ) -> None:

        def decorator(field_computation_callback):

            # Registro de la función
            self._compute.register_computed_field(
                model_name,
                'char',
                FIELD_NAME.DISPLAY_NAME,
                FIELD_LABEL.DISPLAY_NAME,
                field_computation_callback,
            )

            return field_computation_callback

        return decorator

    def register_computed_field(
        self,
        model_name: Union[ModelName, _M],
        field_name: str,
        label: str,
        ttype: TTypeName,
    ) -> None:

        if field_name == FIELD_NAME.DISPLAY_NAME:
            raise IlegalComputedFieldRegistration(
                f'Usa el método {self.assign_display_name.__name__} para registrar una función para nombre visible.'
            )

        def decorator(field_computation_callback):

            # Registro de la función
            self._compute.register_computed_field(
                model_name,
                ttype,
                field_name,
                label,
                field_computation_callback,
            )

            return field_computation_callback

        return decorator

    def register_action(
        self,
        model_name: Union[ModelName, _M],
        action_name: str,
    ) -> None:

        # Creación del decorador que registrará la automatización
        def decorator(action_callbacK: ActionCallback):

            # Registro de la acción
            self._actions.register_action(
                model_name,
                action_name,
                action_callbacK,
            )

            return action_callbacK

        # Retorno del decorador
        return decorator

    def register_automation(
        self,
        model_name: Union[ModelName, _M],
        transation: WriteTransactionName,
        fields: list[str] = [FIELD_NAME.ID],
        execute_if: CriteriaStructure = [],
        method: ExecutionMethod = 'record',
    ):
        """
        ### Registro de automatización
        Este decorador permite registrar una automatización en la instancia del
        módulo.
        Ejemplo de uso:
        >>> @lylac.register_automation(
        >>>     # Modelo donde se ejecutará la automatización
        >>>     'base.users',
        >>>     # La automatización se ejecuta tras crearse un registro
        >>>     'create',
        >>>     # Campos del registro a usar en la automatización
        >>>     ['id'],
        >>> )
        >>> def create_welcome_tasks(ctx) -> None:
        >>>     # Obtención de la ID del registro
        >>>     record_id = ctx.data['id']
        >>>     # Creación de los datos usando una función personalizada
        >>>     tasks_data = build_initial_tasks(record_id)
        >>>     # Creación de los datos en la base de datos
        >>>     ctx.create('project.task', tasks_data)

        #### Tipado dinámico
        Puede utilizarse también un tipado dedicado para mejorar el flujo de desarrollo
        de la función a registrar en el decorador:
        >>> from lylac.utils import Context, BaseRecordData
        >>> 
        >>> # Representación de una tabla personalizada
        >>> class AdminReportJournal(BaseRecordData):
        >>>     title: str
        >>>     user_id: int
        >>>     notes: str
        >>>     state: Literal['open', 'paused', 'closed']
        >>>     involved_users: list[int]
        >>> 
        >>> @lylac.register_automation(
        >>>     # Modelo donde se ejecutará la automatización
        >>>     'admin.report.journal',
        >>>     # La automatización se ejecuta tras crearse un registro
        >>>     'create',
        >>>     # Campos del registro a usar en la automatización
        >>>     ['title', 'notes', 'user_id'],
        >>> )
        >>> def create_new_report_task(
        >>>     ctx: Context.Individual[AdminReportJournal],
        >>> ) -> None:
        >>> 
        >>>     # Obtención del título del reporte
        >>>     report_title = ctx.data['title']
        >>>     # Obtención de las notas del reporte
        >>>     report_notes = ctx.data['notes']
        >>>     # Obtención de la ID del usuario
        >>>     user_id = ctx.data['user_id']
        >>>     # Creación de la tarea
        >>>     ctx.create(
        >>>         'proyect.task',
        >>>         {
        >>>             'title': report_title,
        >>>             'description': report_notes,
        >>>             'user_id': user_id,
        >>>         },
        >>>     )

        De esta manera el editor de código realizará el autocompletado al acceder a
        las llaves de la información.

        Se utiliza el tipado de `Context.Individual` que indica que la automatización
        se ejecuta por registro (creado, en este caso) para ejecutar el código de la
        función. Seguido de ésta, se utiliza el acceso de índice para especificar el
        tipo de registro que se va a recibir, en este caso, se usa la representación de
        una tabla personalizada que pertenecería al modelo `admin.report.journal`.
        >>> def create_new_report_task(
        >>>     # Construcción del tipado
        >>>     ctx: Context.Individual[AdminReportJournal],
        >>> ) -> None:

        #### Nota:
        En el argumento `fields` se debe especificar qué campos se van a utilizar
        en la lectura del registro dentro de la automatización. Esto es
        indispensable para reducir las cargas de información solicitadas a la base
        de datos.
        """

        # Creación del decorador que registrará la automatización
        def decorator(new_automation: Callable[[AutomationContext.Group | AutomationContext.Individual], None]):

            # Registro de la automatización en la estructura central
            self._automations.register_automation(
                model_name,
                transation,
                new_automation,
                fields,
                execute_if,
                method,
            )

            return new_automation

        # Retorno del decorador
        return decorator

    def action(
        self,
        user_id: int,
        model_name: Union[ModelName, _M],
        action_name: str,
        record_id: int,
    ) -> None:

        # Ejecución de la acción
        self._actions.run_action(
            user_id,
            model_name,
            action_name,
            record_id,
        )

    def create(
        self,
        user_id: int,
        model_name: Union[ModelName, _M],
        data: RecordData | list[RecordData],
    ) -> list[int]:
        """
        ### Creación de registros
        Este método realiza la creación de uno o muchos registros a partir del
        nombre de un modelo proporcionado y un diccionario (un único registro)
        o una lista de diccionarios (muchos registros).

        Uso:
        >>> # Para un solo registro
        >>> record = {
        >>>     'login': 'onnymm',
        >>>     'name': 'Onnymm Azzur',
        >>> }
        >>> 
        >>> lylac.create(user_id, 'base.users', record)
        >>> #    id   login          name
        >>> # 0   2  onnymm  Onnymm Azzur
        >>> 
        >>> # Para muchos registros
        >>> records = [
        >>>     {
        >>>         'login': 'onnymm',
        >>>         'name': 'Onnymm Azzur',
        >>>     },
        >>>     {
        >>>         'login': 'lumii',
        >>>         'name': 'Lumii Mynx',
        >>>     },
        >>> ]
        >>> 
        >>> lylac.create(user_id, 'base.users', records)
        >>> #    id   login          name
        >>> # 0   2  onnymm  Onnymm Azzur
        >>> # 1   3   lumii    Lumii Mynx
        """

        # Validación de permiso de transacción
        self._access.check_permission(user_id, model_name, 'create')
        # Preprocesamiento de datos en creación y creación de funciones poscreación
        ( data, post_creation_callback ) = self._preprocess.process_data_on_create(user_id, model_name, data)
        # Ejecución de validaciones
        self._validations.run_validations_on_create(model_name, data)
        # Creación de los registros y obtención de las IDs creadas
        created_records = self._dml.create(model_name, data)
        # Ejecución de las automatizaciones correspondientes
        self._automations.run_after_transaction(
            model_name,
            'create',
            created_records,
            user_id,
        )
        # Ejecución de la función poscreación
        post_creation_callback(created_records)

        return created_records

    def search(
        self,
        user_id: int,
        model_name: Union[ModelName, _M],
        search_criteria: CriteriaStructure = [],
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[int]:
        """
        ### Búsqueda de registros
        Este método retorna todos los registros de una tabla o los registros que cumplan
        con la condición de búsqueda provista, además de segmentar desde un índice
        inicial de desfase y/o un límite de cantidad de registros retornada.

        Uso:
        >>> # Ejemplo 1
        >>> lylac.search(user_id, 'base.users')
        >>> # [1, 2, 3, 4, 5]
        >>> 
        >>> # Ejemplo 2
        >>> lylac.search(user_id, 'base.model.field', [('create_uid', '=', 2)])
        >>> # [7, 9, 12, 13, 17, 21, ...]

        ----
        ### Estructura de criterio de búsqueda
        La estructura del criterio de búsqueda consiste en una lista de dos tipos de
        dato:
        - `TripletStructure`: Estructura de tripletas para queries SQL
        - `LogicOperator`: Operador lógico

        Estas tuplas deben contenerse en una lista. En caso de haber más de una condición, se deben
        unir por operadores lógicos `'AND'` u `'OR'`. Siendo el operador lógico el que toma la
        primera posición:
        >>> ['&', ('amount', '>', 500), ('name', 'ilike', 'as')]
        >>> # "amount" es mayor a 500 y "name" contiene "as"
        >>> ['|', ('id', '=', 5), ('state', '=', 'posted')]
        >>> # "id" es igual a 5 o "state" es igual a "posted"

        ----
        #### Operador lógico
        Tipo de dato que representa un operador lógico.

        Los operadores lógicos disponibles son:
        - `'&'`: AND
        - `'|'`: OR

        ----
        #### Estructura de tripletas para queries SQL
        Este tipo de dato representa una condición sencilla para usarse en una
        transacción en base de datos.

        La estructura de una tripleta consiste en 3 diferentes parámetros:
        1. Nombre del campo del modelo
        2. Operador de comparación
        3. Valor de comparación

        Algunos ejemplos de tripletas son:
        >>> ('name', '=', 'Onnymm')
        >>> # Nombre es igual a "Onnymm"
        >>> ('id', '=', 5)
        >>> # ID es igual a 5
        >>> ('amount', '>', 500)
        >>> # "amount" es mayor a 500
        >>> ('name', 'ilike', 'as')
        >>> # "name" contiene "as"

        ----
        #### Desfase de registros para paginación
        Este parámetro sirve para retornar los registros a partir del índice indicado por éste. Suponiendo que
        una búsqueda normal arrojaría los siguientes resultados:
        >>> lylac.search(user_id, 'base.users')
        >>> # [1, 2, 3, 4, 5, 6, 7]

        Se puede especificar que el retorno de los registros considerará solo a partir desde cierto registro, como
        por ejemplo lo siguiente:
        >>> lylac.search(user_id, 'base.users', offset= 2)
        >>> # [3, 4, 5, 6, 7]

        ----
        #### Límite de registros retornados para paginación
        También es posible establecer una cantidad máxima de registros desde la base de datos. Suponiendo que una
        búsqueda normal arrojaría los siguientes registros:
        >>> lylac.search(user_id, 'base.users')
        >>> # [3, 4, 5, 6, 7]

        Se puede especificar que solo se requiere obtener una cantidad máxima de registros a partir de un
        número provisto:
        >>> lylac.search(user_id, 'base.users', limit= 3)
        >>> # [1, 2, 3]
        """

        # Validación de permiso de transacción
        self._access.check_permission(user_id, model_name, 'read')
        # Búsqueda de registros
        found_ids = self._dql.search(
            model_name,
            search_criteria,
            offset,
            limit,
        )
        return found_ids

    def get_value(
        self,
        user_id: int,
        model_name: Union[ModelName, _M],
        record_id: int,
        field: str,
    ) -> RecordValue:
        """
        ### Obtención de un valor
        Este método retorna el valor especificado de un registro en la base de
        datos a partir de una ID proporcionada y el campo del que se desea
        obtener su valor.

        Uso:
        >>> # Ejemplo 1
        >>> lylac.get_value(user_id, 'base.users', 2, 'name')
        >>> # 'onnymm'
        >>> 
        >>> # Ejemplo 2
        >>> lylac.get_value(user_id, 'base.permissions', 5, 'create_date')
        >>> # '2025-07-01 10:00:00'
        """

        # Validación de permiso de transacción
        self._access.check_permission(user_id, model_name, 'read')

        # Obtención del único elemento contenido en la lista
        [ value ] = (
            # Se utiliza el método de lectura con el registro específico
            self.read(
                user_id,
                model_name,
                record_id,
                [field],
                output_format= 'dataframe',
                only_ids_in_relations= True,
            )
            # Se accede a la columna
            [field]
            # Se convierte la serie de una lista de un elemento
            .to_list()
        )

        return value

    def get_values(
        self,
        user_id: int,
        model_name: Union[ModelName, _M],
        record_id: int,
        fields: list[str],
    ) -> tuple:
        """
        ### Obtención de valores
        Este método retorna los valores especificados de un registro en la base
        de datos a partir de una ID proporcionada y los campos de los cuales se
        desea obtener sus valores.

        Uso:
        >>> # Ejemplo 1
        >>> lylac.get_values(user_id, 'base.users', 1, ['name', 'create_date'])
        >>> # ('onnymm', '2024-11-04 11:16:59')
        >>> 
        >>> # Ejemplo 2
        >>> lylac.get_values(user_id, 'base.permissions', 5, ['label', 'create_uid'])
        >>> # ('Valores de selección de campos / Administrador', 3)
        """

        # Validación de permiso de transacción
        self._access.check_permission(user_id, model_name, 'read')

        # Obtención de la lista de valores
        values = (
            # Se utiliza el método de lectura con el registro específico
            self.read(
                user_id,
                model_name,
                record_id,
                fields,
                output_format= 'dataframe',
                only_ids_in_relations= True,
            )
            # Se accede a la columna
            [fields]
            # Se transpone el DataFrame
            .T
            # Se accede a la columna creada
            [0]
            # Se convierte la serie de una lista de valores
            .to_list()
        )

        # Se convierte el resultado a tupla
        values = tuple(values)

        return values

    def read(
        self,
        user_id: int,
        model_name: Union[ModelName, _M],
        record_ids: int | list[int],
        fields: list[DynamicModelField] = [],
        sortby: str | list[str] = None,
        ascending: bool | list[bool] = True,
        output_format: OutputOptions | None = None,
        only_ids_in_relations: bool = False,
    ) -> pd.DataFrame | list[dict[str, RecordValue]]:
        """
        ### Lectura de registros
        Este método retorna un DataFrame con el contenido de los registros de
        una tabla de la base de datos a partir de una lista de IDs, en el orden
        en el que se especificaron los campos o todos los campos en caso de no
        haber sido especificados.

        Uso:
        >>> # Ejemplo 1
        >>> lylac.search_read(user_id, 'base.users', [2])
        >>> #    id   login          name         create_date          write_date
        >>> # 0   2  onnymm  Onnymm Azzur 2024-11-04 11:16:59 2024-11-04 11:16:59
        >>> 
        >>> lylac.search_read(user_id, 'base.users', [2, 3])
        >>> #    id   login          name         create_date          write_date
        >>> # 0   2  onnymm  Onnymm Azzur 2024-11-04 11:16:59 2024-11-04 11:16:59
        >>> # 1   3   lumii    Lumii Mynx 2024-11-04 11:16:59 2024-11-04 11:16:59
        >>> 
        >>> # Ejemplo 3
        >>> lylac.search_read(user_id, 'base.users', [2, 3], ['user', 'create_date'])
        >>> #    id         name         create_date
        >>> # 0   2 Onnymm Azzur 2024-11-04 11:16:59
        >>> # 1   3   Lumii Mynx 2024-11-04 11:16:59
        """

        # Validación de permiso de transacción
        self._access.check_permission(user_id, model_name, 'read')
        # Conversión de datos entrantes si es necesaria
        record_ids = self._preprocess.convert_to_list(record_ids)
        # Lectura de datos
        data = self._dql.read(
            model_name,
            record_ids,
            fields,
            sortby,
            ascending,
            output_format,
            only_ids_in_relations,
        )

        return data

    def search_read(
        self,
        user_id: int,
        model_name: Union[ModelName, _M],
        search_criteria: CriteriaStructure = [],
        fields: list[DynamicModelField] = [],
        offset: int | None = None,
        limit: int | None = None,
        sortby: str | list[str] | None = None,
        ascending: bool | list[bool] = True,
        output_format: OutputOptions | None = None,
        only_ids_in_relations: bool = False,
    ) -> pd.DataFrame | dict[str, RecordValue]:
        """
        ### Búsqueda y lectura de registros
        Este método retorna un DataFrame con el contenido de los registros de una
        tabla de la base de datos, en el orden en el que se especificaron los campos
        o todos los campos en caso de no haber sido especificados.

        Uso:
        >>> # Ejemplo 1
        >>> lylac.search_read(user_id, 'base.users')
        >>> #    id   login          name         create_date          write_date
        >>> # 0   2  onnymm  Onnymm Azzur 2024-11-04 11:16:59 2024-11-04 11:16:59
        >>> # 1   3   lumii    Lumii Mynx 2024-11-04 11:16:59 2024-11-04 11:16:59
        >>> 
        >>> # Ejemplo 2
        >>> lylac.search_read(user_id, 'base.users', [('user', '=', 'onnymm')])
        >>> #    id   login          name         create_date          write_date
        >>> # 0   2  onnymm  Onnymm Azzur 2024-11-04 11:16:59 2024-11-04 11:16:59
        >>> 
        >>> # Ejemplo 3
        >>> lylac.search_read(user_id, 'base.users', [], ['user', 'create_date'])
        >>> #    id         name         create_date
        >>> # 0   2 Onnymm Azzur 2024-11-04 11:16:59
        >>> # 1   3   Lumii Mynx 2024-11-04 11:16:59

        ----
        ### Estructura de criterio de búsqueda
        La estructura del criterio de búsqueda consiste en una lista de dos tipos de
        dato:
        - `TripletStructure`: Estructura de tripletas para queries SQL
        - `LogicOperator`: Operador lógico

        Estas tuplas deben contenerse en una lista. En caso de haber más de una condición, se deben
        unir por operadores lógicos `'AND'` u `'OR'`. Siendo el operador lógico el que toma la
        primera posición:
        >>> ['&', ('amount', '>', 500), ('name', 'ilike', 'as')]
        >>> # "amount" es mayor a 500 y "name" contiene "as"
        >>> ['|', ('id', '=', 5), ('state', '=', 'posted')]
        >>> # "id" es igual a 5 o "state" es igual a "posted"

        ----
        #### Operador lógico
        Tipo de dato que representa un operador lógico.

        Los operadores lógicos disponibles son:
        - `'&'`: AND
        - `'|'`: OR

        ----
        #### Estructura de tripletas para queries SQL
        Este tipo de dato representa una condición sencilla para usarse en una
        transacción en base de datos.

        La estructura de una tripleta consiste en 3 diferentes parámetros:
        1. Nombre del campo del modelo
        2. Operador de comparación
        3. Valor de comparación

        Algunos ejemplos de tripletas son:
        >>> ('name', '=', 'Onnymm')
        >>> # Nombre es igual a "Onnymm"
        >>> ('id', '=', 5)
        >>> # ID es igual a 5
        >>> ('amount', '>', 500)
        >>> # "amount" es mayor a 500
        >>> ('name', 'ilike', 'as')
        >>> # "name" contiene "as"

        ----
        ### Desfase de registros para paginación
        Este parámetro sirve para retornar los registros a partir del índice indicado por éste. Suponiendo que
        una búsqueda normal arrojaría los siguientes resultados:
        >>> lylac.search_read(user_id, 'base.users')
        >>> #    id    login                  name
        >>> # 0   3   onnymm          Onnymm Azzur
        >>> # 1   4    lumii            Lumii Mynx
        >>> # 2   5  user001  Persona Sin Nombre 1
        >>> # 3   6  user002  Persona Sin Nombre 2
        >>> # 4   7  user003  Persona Sin Nombre 3

        Se puede especificar que el retorno de los registros considerará solo a partir desde cierto registro, como
        por ejemplo lo siguiente:
        >>> lylac.search_read(user_id, 'base.users', offset= 2)
        >>> # 1   4    lumii            Lumii Mynx
        >>> # 2   5  user001  Persona Sin Nombre 1
        >>> # 3   6  user002  Persona Sin Nombre 2
        >>> # 4   7  user003  Persona Sin Nombre 3

        ----
        ### Límite de registros retornados para paginación
        También es posible establecer una cantidad máxima de registros desde la base de datos. Suponiendo que una
        búsqueda normal arrojaría los siguientes registros:
        >>> lylac.search_read(user_id, 'base.users')
        >>> #    id    login                  name
        >>> # 0   3   onnymm          Onnymm Azzur
        >>> # 1   4    lumii            Lumii Mynx
        >>> # 2   5  user001  Persona Sin Nombre 1
        >>> # 3   6  user002  Persona Sin Nombre 2
        >>> # 4   7  user003  Persona Sin Nombre 3

        Se puede especificar que solo se requiere obtener una cantidad máxima de registros a partir de un
        número provisto:
        >>> lylac.search_read(user_id, 'base.users', limit= 3)
        >>> #    id    login                  name
        >>> # 0   3   onnymm          Onnymm Azzur
        >>> # 1   4    lumii            Lumii Mynx
        >>> # 2   5  user001  Persona Sin Nombre 1
        """

        # Validación de permiso de transacción
        self._access.check_permission(user_id, model_name, 'read')
        # Búsqueda y lectura de datos
        data = self._dql.search_read(
            model_name,
            search_criteria,
            fields,
            offset,
            limit,
            sortby,
            ascending,
            output_format,
            only_ids_in_relations,
        )

        return data

    def search_count(
        self,
        user_id: int,
        model_name: Union[ModelName, _M],
        search_criteria: CriteriaStructure = [],
    ) -> int:
        """
        ### Búsqueda y conteo de resultados
        Este método retorna el conteo de de todos los registros de una tabla o los
        registros que cumplan con la condición de búsqueda provista, ideal para funcionalidades
        de paginación que muestran un total de registros.

        Uso:
        >>> # Ejemplo 1
        >>> lylac.search_count(user_id, 'base.users')
        >>> # 5
        >>> 
        >>> # Ejemplo 2
        >>> lylac.search_count(user_id, 'base.permissions', [('create_uid', '=', 5)])
        >>> # 126

        ----
        ### Estructura de criterio de búsqueda
        La estructura del criterio de búsqueda consiste en una lista de dos tipos de
        dato:
        - `TripletStructure`: Estructura de tripletas para queries SQL
        - `LogicOperator`: Operador lógico

        Estas tuplas deben contenerse en una lista. En caso de haber más de una condición, se deben
        unir por operadores lógicos `'AND'` u `'OR'`. Siendo el operador lógico el que toma la
        primera posición:
        >>> ['&', ('amount', '>', 500), ('name', 'ilike', 'as')]
        >>> # "amount" es mayor a 500 y "name" contiene "as"
        >>> ['|', ('id', '=', 5), ('state', '=', 'posted')]
        >>> # "id" es igual a 5 o "state" es igual a "posted"

        ----
        #### Operador lógico
        Tipo de dato que representa un operador lógico.

        Los operadores lógicos disponibles son:
        - `'&'`: AND
        - `'|'`: OR

        ----
        #### Estructura de tripletas para queries SQL
        Este tipo de dato representa una condición sencilla para usarse en una
        transacción en base de datos.

        La estructura de una tripleta consiste en 3 diferentes parámetros:
        1. Nombre del campo del modelo
        2. Operador de comparación
        3. Valor de comparación

        Algunos ejemplos de tripletas son:
        >>> ('name', '=', 'Onnymm')
        >>> # Nombre es igual a "Onnymm"
        >>> ('id', '=', 5)
        >>> # ID es igual a 5
        >>> ('amount', '>', 500)
        >>> # "amount" es mayor a 500
        >>> ('name', 'ilike', 'as')
        >>> # "name" contiene "as"
        """

        # Validación de permiso de transacción
        self._access.check_permission(user_id, model_name, 'read')
        # Conteo de registros
        count = self._dql.search_count(model_name, search_criteria)

        return count

    def update(
        self,
        user_id: int,
        model_name: Union[ModelName, _M],
        record_ids: int | list[int],
        data: RecordData,
    ) -> bool:
        """
        ### Actualización de registros
        Este método realiza la actualización de uno o más registros a partir de su respectiva
        ID provista, actualizando uno o más campos con el valor provisto. Este método solo
        sobreescribe un mismo valor por cada campo a todos los registros provistos.

        Uso:
        >>> lylac.search_read(user_id, 'base.users', fields= ['login', 'name'])
        >>> #    id    login                  name
        >>> # 0   3   onnymm          Onnymm Azzur
        >>> # 1   4    lumii            Lumii Mynx
        >>> # 2   5  user001  Persona Sin Nombre 1
        >>> # 3   6  user002  Persona Sin Nombre 2
        >>> # 4   7  user003  Persona Sin Nombre 3
        >>> 
        >>> # Modificación
        >>> lylac.update(user_id, 'base.users', [3, 4, 5], {'name': 'Cambiado'})
        >>> # True
        >>> lylac.search_read(user_id, 'base.users', fields= ['login', 'name'])
        >>> #    id    login                  name
        >>> # 0   3   onnymm              Cambiado
        >>> # 1   4    lumii              Cambiado
        >>> # 2   5  user001              Cambiado
        >>> # 3   6  user002  Persona Sin Nombre 2
        >>> # 4   7  user003  Persona Sin Nombre 3
        """

        # Conversión de entrada de datos a lista de datos
        record_ids = self._preprocess.convert_to_list(record_ids)
        # Ejecución del método UPDATE WHERE
        return self.update_where(
            user_id,
            model_name,
            [('id', 'in', record_ids)],
            data,
            record_ids,
        )

    def update_where(
        self,
        user_id: int,
        model_name: Union[ModelName, _M],
        search_criteria: CriteriaStructure,
        data: RecordData,
        _record_ids: list[int] = []
    ) -> bool:
        """
        ### Actualización de registros donde...
        Este método realiza la actualización de uno o más registros a partir de una
        condición provista, actualizando uno o más campos con el valor provisto. Este
        método solo sobreescribe un mismo valor por cada campo a todos los registros
        encontrados en base a la condición provista.

        Uso:
        >>> lylac.search_read(user_id, 'base.users', fields= ['login', 'name'])
        >>> #    id    login                  name
        >>> # 0   3   onnymm          Onnymm Azzur
        >>> # 1   4    lumii            Lumii Mynx
        >>> # 2   5  user001  Persona Sin Nombre 1
        >>> # 3   6  user002  Persona Sin Nombre 2
        >>> # 4   7  user003  Persona Sin Nombre 3
        >>> 
        >>> # Modificación
        >>> lylac.update(user_id, 'base.users', [('name', 'ilike', 'sin nombre')], {'name': 'Zopilote'})
        >>> #    id    login          name
        >>> # 0   3   onnymm  Onnymm Azzur
        >>> # 1   4    lumii    Lumii Mynx
        >>> # 2   5  user001      Zopilote
        >>> # 3   6  user002      Zopilote
        >>> # 4   7  user003      Zopilote
        """

        # Validación de permiso de transacción
        self._access.check_permission(user_id, model_name, 'update')
        # Ejecución de validaciones
        self._validations.run_validations_on_update(model_name, search_criteria, data)
        # Preprocesamiento de datos en actualización y obtención de función posactualización
        after_update_callback = self._preprocess.process_data_on_update(user_id, model_name, _record_ids, data)
        # Actualización de registros
        updated_records = self._dml.update_where(model_name, search_criteria, data)
        # Ejecución de las automatizaciones correspondientes
        self._automations.run_after_transaction(
            model_name,
            'update',
            updated_records,
            user_id,
        )
        # Ejecución de función posactualización
        after_update_callback()

        return True

    def delete(
        self,
        user_id: int,
        model_name: Union[ModelName, _M],
        record_ids: int | list[int]
    ) -> bool:
        """
        ## Eliminación de registros
        Este método realiza la eliminación de uno o más registros de la base datos a partir de
        su respectiva ID provista.

        Uso:
        >>> #    id     user                  name
        >>> # 0   3   onnymm          Onnymm Azzur
        >>> # 1   4    lumii            Lumii Mynx
        >>> # 2   5  user001  Persona Sin Nombre 1
        >>> # 3   6  user002  Persona Sin Nombre 2
        >>> # 4   7  user003  Persona Sin Nombre 3
        >>> 
        >>> # Eliminación
        >>> db.delete("users", 3)
        >>> #    id     user                  name
        >>> # 1   4    lumii            Lumii Mynx
        >>> # 2   5  user001  Persona Sin Nombre 1
        >>> # 3   6  user002  Persona Sin Nombre 2
        >>> # 4   7  user003  Persona Sin Nombre 3
        """

        # Validación de permiso de transacción
        self._access.check_permission(user_id, model_name, 'delete')
        # Ejecución de validaciones
        self._validations.run_validations_on_delete(model_name, record_ids)
        # Conversión de datos entrantes si es necesaria
        record_ids = self._preprocess.convert_to_list(record_ids)
        # Creación de función de ejecución de automatizaciones
        run_post_delete_automations = self._automations.generate_before_transaction(
            model_name,
            record_ids,
            user_id,
        )
        # Eliminación de registros
        deleted_ids = self._dml.delete(model_name, record_ids)
        # Ejecución de las automatizaciones correspondientes
        run_post_delete_automations(deleted_ids)

        return True

    def and_(
        self,
        cs_1: CriteriaStructure,
        cs_2: CriteriaStructure
    ) -> CriteriaStructure:

        # Si los dos criterios de búsqueda contienen datos
        if len(cs_1) and len(cs_2):

            # Se retornan los criterios de búsqueda unidos por operador `and`
            res: CriteriaStructure = ['&', *cs_1, *cs_2]
            return res

        # Si sólo el primer criterio de búsqueda contiene datos...
        elif len(cs_1):
            # Se retorna sólo el primer criterio de búsqueda
            return cs_1
        """
        ## Método para unir dos criterios de búsqueda por medio de un operador `'&'`.

        Uso:
        >>> # Ejemplo 1
        >>> cs_1 = [('invoice_line_id', '=', 5)]
        >>> cs_2 = [('state', '=', 'sent')]
        >>> merged_cs = lylac.and_(cs_1, cs_2)
        >>> # ['&', ('invoice_line_id', '=', 5), ('state', '=', 'sent')]
        >>> 
        >>> # Ejemplo 2
        >>> cs_1 = [('invoice_line_id', '=', 5)]
        >>> cs_2 = ['|', ('state', '=', 'posted'), ('state', '=', 'sent')]
        >>> merged_cs = lylac.and_(cs_1, cs_2)
        >>> # ['&', ('invoice_line_id', '=', 5), '|', ('state', '=', 'posted'), ('state', '=', 'sent')]
        """

    def or_(
        self,
        cs_1: CriteriaStructure,
        cs_2: CriteriaStructure
    ) -> CriteriaStructure:
        """
        ## Método de clase para unir dos criterios de búsqueda por medio de un operador `'|'`.

        Uso:
        >>> # Ejemplo 1
        >>> cs_1 = [('invoice_line_id', '=', 5)]
        >>> cs_2 = [('state', '=', 'sent')]
        >>> merged_cs = DMLManager.or_(cs_1, cs_2)
        >>> # ['|', ('invoice_line_id', '=', 5), ('state', '=', 'sent')]
        >>> 
        >>> # Ejemplo 2
        >>> cs_1 = [('invoice_line_id', '=', 5)]
        >>> cs_2 = ['|', ('state', '=', 'posted'), ('state', '=', 'sent')]
        >>> merged_cs = DMLManager.or_(cs_1, cs_2)
        >>> # ['|', ('invoice_line_id', '=', 5), '|', ('state', '=', 'posted'), ('state', '=', 'sent')]
        """

        # Si los dos criterios de búsqueda contienen datos
        if len(cs_1) and len(cs_2):

            # Se retornan los criterios de búsqueda unidos por operador `or`
            res: CriteriaStructure = ['|', *cs_1, *cs_2]
            return res

        # Si sólo el primer criterio de búsqueda contiene datos...
        elif len(cs_1):
            # Se retorna sólo el primer criterio de búsqueda
            return cs_1
