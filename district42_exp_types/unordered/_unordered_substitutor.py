from typing import Any, cast

from niltype import Nil
from revolt import Substitutor

from ._unordered_schema import UnorderedSchema

__all__ = ("UnorderedSubstitutor",)


class UnorderedSubstitutor(Substitutor, extend=True):
    def visit_unordered(self, schema: UnorderedSchema, *,
                        value: Any = Nil,
                        **kwargs: Any) -> UnorderedSchema:
        return cast(UnorderedSchema, self.visit_list(schema, value=value, **kwargs))
