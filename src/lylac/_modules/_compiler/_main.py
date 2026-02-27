from sqlalchemy import (
    and_,
    delete,
    distinct,
    select,
    update,
    func,
)
from sqlalchemy.orm import (
    Session,
    aliased,
)
from ..._constants import (
    MODEL_NAME,
    FIELD_NAME,
)
from ..._core.main import _Lylac_Core
from ..._core.modules import Compiler_Core
from ..._module_types import (
    RecordData,
    ModelName,
    TransactionName,
)

class Compiler(Compiler_Core):

    def __init__(
        self,
        instance: _Lylac_Core
    ):

        # Asignación de la instancia principal
        self._main = instance
        # Asignación de la instancia de estructura interna
        self._strc = instance._strc
        # Asignación de la instancia de índice
        self._index = instance._index
        # Asignación de la instancia de conexión
        self._connection = instance._connection
        # Asignación del motor de conexión
        self._engine = instance._engine

    def get_user_data_by_username(
        self,
        login: str,
    ) -> tuple[int, str] | None:

        # Obtención de la tabla de usuarios
        base_users = self._strc.get_model(MODEL_NAME.BASE_USERS)
        # Obtención de las instancias de columna
        base_users__id = self._index[base_users]['id']
        base_users__password = self._index[base_users]['password']
        base_users__login = self._index[base_users]['login']
        base_users__active = self._index[base_users]['active']

        # Creación del query
        stmt = (
            select(
                base_users__id,
                base_users__password,
            )
            .where(
                base_users__login == login,
                base_users__active == True,
            )
        )

        # Ejecución de la transacción
        response = self._connection.execute(stmt)
        # Obtención de los datos encontrados
        found_data = response.fetchall()

        # Si no hay datos...
        if not found_data:
            # Se retorna None
            return None

        # Destructuración de los datos
        [ ( user_id, hashed_password ) ] = found_data

        return ( user_id, hashed_password )

    def is_active_user_from_session_uuid(
        self,
        session_uuid: str,
    ) -> bool:

        # Obtención de los modelos
        base_users_session = self._strc.get_model(MODEL_NAME.BASE_USERS_SESSION)
        base_users = aliased( self._strc.get_model(MODEL_NAME.BASE_USERS) )
        # Obtención de las instancias de columnas
        base_users_session__user_id = self._index[base_users_session]['user_id']
        base_users_session__uuid = self._index[base_users_session]['name']
        base_users__id = self._index[base_users]['id']
        base_users__active = self._index[base_users]['active']

        # Creación del query
        stmt = (
            select(
                base_users__active
            )
            .select_from(base_users_session)
            .outerjoin(
                base_users,
                base_users_session__user_id == base_users__id,
            )
            .where(base_users_session__uuid == session_uuid)
        )

        # Ejecución en la base de datos
        response = self._connection.execute(stmt)
        # Destructuración del resultado
        [ ( is_active, ) ] = response.fetchall()

        return is_active

    def create_many2many(
        self,
        model_name: ModelName,
        data: list[RecordData],
    ) -> None:

        # Obtención del modelo
        model_model = self._strc.get_model(model_name)
        # Inicialización de los datos
        instanced_data = [ model_model(**record) for record in data ]

        # Creación de registros en la base de datos
        with Session(self._engine) as session:
            session.add_all(instanced_data)
            session.commit()

    def link_many2many(
        self,
        model_name: ModelName,
        field_name: str,
        parent_record_ids: list[int],
        children_record_ids: list[int],
    ) -> None:

        # Obtención del modelo de tabla de relación
        model_model = self._strc.get_relation_model(model_name, field_name)
        # Inicialización de los datos
        data = [
            {
                'x': parent_record_id,
                'y': record_id,
            } for parent_record_id in parent_record_ids
            for record_id in children_record_ids
        ]
        # Se crean los objetos instanciados
        instanced_data = [ model_model(**record) for record in data ]

        # Creación de registros en la base de datos
        with Session(self._engine) as session:
            session.add_all(instanced_data)
            session.commit()

    def unlink_many2many(
        self,
        model_name: ModelName,
        field_name: str,
        parent_record_ids: list[int],
        children_record_ids: list[int],
    ) -> None:

        # Obtención de modelo de tabla de relación
        model_model = self._strc.get_relation_model(model_name, field_name)
        # Obtención de instancia de campo de ID de modelo propietario
        x_field_instance = self._index[model_model]['y']
        y_field_instance = self._index[model_model]['x']

        # Creación del query
        stmt = (
            delete(model_model)
            .where(
                and_(
                    x_field_instance.in_(parent_record_ids),
                    y_field_instance.in_(children_record_ids),
                )
            )
        )

        # Ejecución de la transacción en la base de datos
        self._connection.execute(stmt, commit= True)

    def delete_many2many(
        self,
        model_name: ModelName,
        field_name: str,
        record_ids: list[int],
    ) -> None:

        # Obtención de modelo de tabla de relación
        model_model = self._strc.get_relation_model(model_name, field_name)
        # Obtención de instancia de campo de ID de modelo propietario
        id_field_instance = self._index[model_model]['x']

        # Creación del query
        stmt = (
            delete(model_model)
            .where( id_field_instance.in_(record_ids) )
        )

        # Ejecución de la transacción en la base de datos
        self._connection.execute(stmt, commit= True)

    def check_permission(
        self,
        user_id: int,
        model_name: ModelName,
        transaction: TransactionName,
    ) -> bool:

        # Obtención de los modelos a usar
        base_model = self._strc.get_model('base.model')
        base_users = self._strc.get_model('base.users')
        base_users_role = self._strc.get_model('base.users.role')
        base_model_access_groups = self._strc.get_model('base.model.access.groups')
        base_model_access = self._strc.get_model('base.model.access')
        _rel_base_users__base_users_role = self._strc.get_model('_rel.base_users.base_users_role')
        _rel_base_users_role__base_model_access_groups = self._strc.get_model('_rel.base_users_role.base_model_access_groups')
        _rel_base_model_access_groups__base_model_access = self._strc.get_model('_rel.base_model_access_groups.base_model_access')

        # Obtención de las instancias de columnas principales a usar
        base_model_access__name = self._index[base_model_access]['name']
        base_model_access__perm_create = self._index[base_model_access]['perm_create']
        base_model_access__perm_read = self._index[base_model_access]['perm_read']
        base_model_access__perm_update = self._index[base_model_access]['perm_update']
        base_model_access__perm_delete = self._index[base_model_access]['perm_delete']
        # Obtención de las instancias de columnas a usar en outerjoins
        base_model__id = self._index[base_model]['id']
        base_model__model = self._index[base_model]['model']
        base_users__id = self._index[base_users]['id']
        base_users_role__id = self._index[base_users_role]['id']
        base_model_access_groups__id = self._index[base_model_access_groups]['id']
        base_model_access__id = self._index[base_model_access]['id']
        base_model_access__model_id = self._index[base_model_access]['model_id']
        _rel_base_users__base_users_role__x = self._index[_rel_base_users__base_users_role]['x']
        _rel_base_users__base_users_role__y = self._index[_rel_base_users__base_users_role]['y']
        _rel_base_users_role__base_model_access_groups__x = self._index[_rel_base_users_role__base_model_access_groups]['x']
        _rel_base_users_role__base_model_access_groups__y = self._index[_rel_base_users_role__base_model_access_groups]['y']
        _rel_base_model_access_groups__base_model_access__x = self._index[_rel_base_model_access_groups__base_model_access]['x']
        _rel_base_model_access_groups__base_model_access__y = self._index[_rel_base_model_access_groups__base_model_access]['y']

        # Creación de condición
        permission_condition = {
            'create': base_model_access__perm_create == True,
            'read': base_model_access__perm_read == True,
            'update': base_model_access__perm_update == True,
            'delete': base_model_access__perm_delete == True,
        }

        # Creación del query
        stmt = (
            select(
                # Obtención de valores únicos
                func.count(
                    distinct(base_model_access__name)
                ),
            )
            # Especificación de la tabla de partida
            .select_from(base_users)
            # Unión de tablas
            .outerjoin(
                _rel_base_users__base_users_role,
                base_users__id == _rel_base_users__base_users_role__x,
            )
            .outerjoin(
                base_users_role,
                _rel_base_users__base_users_role__y == base_users_role__id,
            )
            .outerjoin(
                _rel_base_users_role__base_model_access_groups,
                base_users_role__id == _rel_base_users_role__base_model_access_groups__x,
            )
            .outerjoin(
                base_model_access_groups,
                _rel_base_users_role__base_model_access_groups__y == base_model_access_groups__id,
            )
            .outerjoin(
                _rel_base_model_access_groups__base_model_access,
                base_model_access_groups__id == _rel_base_model_access_groups__base_model_access__x,
            )
            .outerjoin(
                base_model_access,
                _rel_base_model_access_groups__base_model_access__y == base_model_access__id,
            )
            .outerjoin(
                base_model,
                base_model_access__model_id == base_model__id,
            )
            # Condiciones
            .where(
                # ID de usuario
                base_users__id == user_id,
                # Permiso a validar
                permission_condition[transaction],
                # Nombre de la tabla
                base_model__model == model_name
            )
        )

        # Ejecución del query
        response = self._connection.execute(stmt)
        # Obtención del conteo de la cantidad de permisos encontrados
        permissions_qty = response.scalar()

        # Se retorna la validación de si existen o no permisos para la transacción a realizar
        return permissions_qty > 0

    def change_password(
        self,
        user_id: int,
        hashed_new_password: str,
    ) -> None:

        # Obtención del modelo de la tabla
        base_users = self._strc.get_model(MODEL_NAME.BASE_USERS)
        # Obtención de la instancia de campo de ID
        c_base_users__id = self._index[base_users][FIELD_NAME.ID]
        # Creación del query
        stmt = (
            update(base_users)
            .where(c_base_users__id == user_id)
            .values({'password': hashed_new_password})
        )
        # Ejecución de la transacción
        self._connection.execute(stmt, commit= True)
