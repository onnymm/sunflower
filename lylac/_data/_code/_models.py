MODEL_TABLE_TEMPLATE = (
"""
class {model_name}(self._base, ModelTemplate):
    __tablename__ = '{model_name}'

data['model'] = {model_name}
"""
)

RELATION_TABLE_TEMPLATE = (
"""
class _rel_{main_model}__{referenced_model}(self._base):
    __tablename__ = '_rel_{main_model}__{referenced_model}'
    x = Column(Integer, ForeignKey("{main_model}.id", ondelete= "CASCADE"), primary_key= True)
    y = Column(Integer, ForeignKey("{referenced_model}.id", ondelete= "CASCADE"), primary_key= True)

data['model'] = _rel_{main_model}__{referenced_model}
"""
)
