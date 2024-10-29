from typing import Any

from d42.validation import ValidationResult, Validator
from niltype import Nil, Nilable
from th import PathHolder

from ._sdict_schema import SDictSchema

__all__ = ("SDictValidator",)


class SDictValidator(Validator, extend=True):
    def visit_sdict(self, schema: SDictSchema, *,
                    value: Any = Nil, path: Nilable[PathHolder] = Nil,
                    **kwargs: Any) -> ValidationResult:
        return self.visit_dict(schema, value=value, path=path, **kwargs)
