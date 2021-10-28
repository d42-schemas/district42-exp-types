from typing import Any, cast

from niltype import Nil
from revolt import Substitutor

# register visit_multi_dict
from district42_exp_types.multi_dict import MultiDictSubstitutor  # noqa: F401

from ._ci_multi_dict_schema import CIMultiDictSchema

__all__ = ("CIMultiDictSubstitutor",)


class CIMultiDictSubstitutor(Substitutor, extend=True):
    def visit_ci_multi_dict(self, schema: CIMultiDictSchema, *,
                            value: Any = Nil, **kwargs: Any) -> CIMultiDictSchema:
        return cast(CIMultiDictSchema, self.visit_multi_dict(schema, value=value, **kwargs))
