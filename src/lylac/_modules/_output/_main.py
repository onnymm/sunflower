from typing import (
    Any,
    Optional,
)
import pandas as pd
from sqlalchemy.engine.cursor import CursorResult
from ..._core.main import _Lylac_Core
from ..._core.modules import Output_Core
from ..._module_types import (
    OutputOptions,
    TTypeName,
)
from ._submodules import (
    _DataTypes,
    _RawORM,
)

class Output(Output_Core):

    def __init__(
        self,
        instance: _Lylac_Core,
        output_format: OutputOptions | None
    ) -> None:

        # Asignación de la instancia propietaria
        self._main = instance

        # Configuración de formato de salida por defecto
        self._default_output = output_format

        # Creación del submódulo de Tipos de dato
        self._m_data = _DataTypes(self)
        # Creación del submódulo de Raw ORM
        self._m_orm = _RawORM(self)

    def get_found_ids(
        self,
        response: CursorResult[int],
    ) -> list[int]:

        # Obtención de los valores
        found_ids: list[int] = [ getattr(row, 'id') for row in response ]

        return found_ids

    def build_output(
        self,
        response: pd.DataFrame,
        ttypes: list[tuple[str, TTypeName]],
        specified_output: OutputOptions,
        default_output: Optional[OutputOptions] = None,
        only_ids_in_relations: bool = False,
    ) -> pd.DataFrame | list[dict[str, Any]]:

        # Obtención de lista de campos
        fields = [ field_name for ( field_name, _ ) in ttypes ]

        # Si el DataFrame de respuesta está vacío...
        if len(response) == 0:
            # Se inicializa un DataFrame con los nombres de campos y se reasigna a `data`
            data = pd.DataFrame(response, columns= fields)
        else:
            # Se reasigna el contenido de variable
            data = response
            # Destructuración e iteración de los atributos de campo
            for ( field_name, ttype ) in ttypes:
                # Si fue solicitado el manejo de solo IDs en campos relacionados...
                if only_ids_in_relations and ttype == 'many2one':
                    # Se manejan los tipos many2one como enteros
                    ttype = 'integer'
                # Recuperación de tipos de dato por columna
                data = self._m_data.recover_ttype[ttype](data, field_name)

            # Selección de columnas
            data = data[fields]

        # Si se especificó una salida para la ejecución actual...
        if specified_output:
            if specified_output == 'dataframe':
                return data
            else:
                return data.to_dict('records')

        # Si existe un formato por defecto en la instancia...
        if self._default_output:
            if self._default_output == 'dataframe':
                return data
            else:
                return data.to_dict('records')

        # Si no se especificó un formato en ejecución o instancia...
        if default_output == 'dataframe':
            return data

        # Retorno de información en lista de diccionarios
        return data.to_dict('records')

    def _recover_ttypes(self, data: pd.DataFrame, table_name: str) -> pd.DataFrame:

        # Obtención del mapa de tipos de dato por campo
        ttypes = self._m_orm.get_fields_ttypes(table_name, data.columns.to_list())

        # Transformación de datos
        for ( field, ttype ) in ttypes.items():
            data = self._m_data.recover_ttype[ttype](data, field)

        return data
