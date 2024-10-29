from typing import Any

from d42.substitution import Substitutor
from d42.substitution.errors import make_substitution_error
from niltype import Nil

from ._numeric_schema import NumericSchema

__all__ = ("NumericSubstitutor",)


class NumericSubstitutor(Substitutor, extend=True):
    def visit_numeric(self, schema: NumericSchema, *,
                      value: Any = Nil, **kwargs: Any) -> NumericSchema:
        result = schema.__accept__(self._validator, value=value)
        if result.has_errors():
            raise make_substitution_error(result, self._formatter)
        return schema.__class__(schema.props.update(value=value))
