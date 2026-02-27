from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.decl_api import DeclarativeBase

class FieldsGetter_Interface():
    _available_model: type[DeclarativeBase]

    def __getitem__(
        self,
        field_name: str,
    ) -> InstrumentedAttribute:
        ...
