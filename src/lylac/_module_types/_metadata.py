from datetime import datetime
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy.types import (
    DateTime,
    Integer,
    String,
)

class ModelTemplate():
    # ID del registro
    id: Mapped[int] = mapped_column(Integer, primary_key= True, autoincrement= True)
    # Nombre o título representativo del registro
    name: Mapped[str] = mapped_column(String(60), nullable= True)
    # Fecha de creación del registro
    create_date: Mapped[datetime] = mapped_column(DateTime, default= datetime.now)
    # Última fecha de modificación del registro
    write_date: Mapped[datetime] = mapped_column(DateTime, default= datetime.now, onupdate= datetime.now)

ModelData = tuple[str, list[dict]]
"""
### Datos de modelo
Estructura de datos usada en la declaración de datos iniciales de la base de
datos conformada por una tupla de un nombre de .

Ejemplo:
>>> (
>>>     'base.model.field',
>>>     [
>>>         {
>>>             'name': 'profile_picture',
>>>             'label': 'Foto de perfil',
>>>             'ttype': 'file',
>>>             'model_id': 4,
>>>             'state': 'base',
>>>         },
>>>     ],
    )
"""
