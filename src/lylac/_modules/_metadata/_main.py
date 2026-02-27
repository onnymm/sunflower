from typing import Optional
from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.types import (
    Boolean,
    String,
    Text,
    LargeBinary,
)
from ..._core.modules import Metadata_Core
from ..._core.main import _Lylac_Core
from ..._module_types import ModelTemplate
from ...security import default_password

class Metadata(Metadata_Core):

    def __init__(
        self,
        instance: _Lylac_Core,
    ) -> None:

        # Asignación de instancia principal
        self._main = instance

        class _Base(DeclarativeBase):
            pass

        class BaseUsers(_Base, ModelTemplate):
            __tablename__ = 'base_users'

            # Inicio de sesión
            login: Mapped[str] = mapped_column(String(60), nullable= False)
            # Contraseña
            password: Mapped[str] = mapped_column(String(255), default= default_password)
            # Es activo
            active: Mapped[bool] = mapped_column(Boolean, default= True)
            # Sincronizar
            sync: Mapped[bool] = mapped_column(Boolean, default= True)
            # Foto de perfil
            profile_picture: Mapped[str] = mapped_column(LargeBinary, nullable= True)

        class BaseModel_(_Base, ModelTemplate):
            __tablename__ = 'base_model'

            # Nombre representativo para usarse en el servidor
            model: Mapped[str] = mapped_column(String(60), nullable= False)
            # Etiqueta del modelo
            label: Mapped[str] = mapped_column(String(60), nullable= False)
            # Descripción del propósito del modelo
            description: Mapped[str] = mapped_column(Text, nullable= True)
            # Tipo de modelo
            state: Mapped[str] = mapped_column(String(60), nullable= False, default= 'generic')

        class BaseModelField(_Base, ModelTemplate):
            __tablename__ = 'base_model_field'

            # ID del modelo al que pertenece
            model_id: Mapped[int] = mapped_column(ForeignKey("base_model.id"), nullable= False)
            # Etiqueta del campo
            label: Mapped[str] = mapped_column(String(60), nullable= False)
            # Tipo de dato del campo
            ttype: Mapped[str] = mapped_column(String(60), nullable= False)
            # El valor del campo puede ser nulo
            nullable: Mapped[bool] = mapped_column(Boolean, default= True)
            # Es requerido
            is_required: Mapped[bool] = mapped_column(Boolean, default= False)
            # Solo lectura
            readonly: Mapped[bool] = mapped_column(Boolean, default= False)
            # Valor inicial
            default_value: Mapped[Optional[str]] = mapped_column(String(255), nullable= True)
            # El valor del campo debe ser único en toda la tabla
            unique: Mapped[bool] = mapped_column(Boolean, default= False)
            # Información de ayuda
            help_info: Mapped[str] = mapped_column(Text, nullable= True)
            # Modelo de relación
            related_model_id: Mapped[Optional[int]] = mapped_column(ForeignKey('base_model.id'), nullable= True)
            # Campo de relación
            related_field: Mapped[str] = mapped_column(String(60), nullable= True)
            # Tipo de modelo
            state: Mapped[str] = mapped_column(String(60), nullable= False, default= 'generic')
            # Modelo computado
            is_computed: Mapped[str] = mapped_column(Boolean, nullable= False, default= False)

            # Relación hacia el modelo al que pertenece
            model: Mapped["BaseModel_"] = relationship(BaseModel_, foreign_keys= [model_id])
            # Relación hacia el modelo relacionado (opcional, si es many2one)
            related_model: Mapped[Optional["BaseModel_"]] = relationship(
                BaseModel_,
                foreign_keys=[related_model_id],
            )

        class BaseModelFieldSelection(_Base, ModelTemplate):
            __tablename__ = 'base_model_field_selection'

            # ID del campo al que pertenece
            field_id: Mapped[int] = mapped_column(ForeignKey('base_model_field.id'), nullable= False)
            # Etiqueta del valor de selección
            label: Mapped[str] = mapped_column(String(60), nullable= False)

        # Se almacena _Base
        self._main._base = _Base

        # Se almacenan los demás modelos para mantenerlos en la memoria de la ejecución
        self._models = [
            BaseUsers,
            BaseModel_,
            BaseModelField,
            BaseModelFieldSelection,
        ]
