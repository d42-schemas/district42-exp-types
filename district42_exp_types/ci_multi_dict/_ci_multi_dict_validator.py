from typing import Any, cast

from niltype import Nil, Nilable
from th import PathHolder
from valera import ValidationResult, Validator

from ._ci_multi_dict_schema import CIMultiDictSchema

__all__ = ("CIMultiDictValidator",)


class CIMultiDictValidator(Validator, extend=True):
    def visit_ci_multi_dict(self, schema: CIMultiDictSchema, *,
                            value: Any = Nil, path: Nilable[PathHolder] = Nil,
                            **kwargs: Any) -> ValidationResult:
        return cast(ValidationResult,
                    self.visit_multi_dict(schema, value=value, path=path, **kwargs))
