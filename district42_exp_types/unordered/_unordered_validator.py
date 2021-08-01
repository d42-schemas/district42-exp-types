from typing import Any

from niltype import Nil, Nilable
from th import PathHolder
from valera import ValidationResult, Validator

from ._unordered_schema import UnorderedSchema

__all__ = ("UnorderedValidator",)


class UnorderedValidator(Validator, extend=True):
    def visit_unordered(self, schema: UnorderedSchema, *,
                        value: Any = Nil, path: Nilable[PathHolder] = Nil,
                        **kwargs: Any) -> ValidationResult:
        return self.visit_list(schema, value=value, path=path, **kwargs)
