from typing import Any

from d42.substitution import Substitutor
from d42.substitution.errors import make_substitution_error
from niltype import Nil

from ._uuid_schema import UUIDSchema

__all__ = ("UUIDSubstitutor",)


class UUIDSubstitutor(Substitutor, extend=True):
    def visit_uuid(self, schema: UUIDSchema, *, value: Any = Nil, **kwargs: Any) -> UUIDSchema:
        result = schema.__accept__(self._validator, value=value)
        if result.has_errors():
            raise make_substitution_error(result, self._formatter)
        return schema.__class__(schema.props.update(value=value))
