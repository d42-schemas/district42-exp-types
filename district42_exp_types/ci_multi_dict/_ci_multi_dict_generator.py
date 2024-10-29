from typing import Any

from d42.declaration import GenericSchema
from d42.generation import Generator
from multidict import CIMultiDict

# register visit_multi_dict
from district42_exp_types.multi_dict import MultiDictGenerator  # noqa: F401

from ._ci_multi_dict_schema import CIMultiDictSchema

__all__ = ("CIMultiDictGenerator",)


class CIMultiDictGenerator(Generator, extend=True):
    def visit_ci_multi_dict(self, schema: CIMultiDictSchema,
                            **kwargs: Any) -> CIMultiDict[GenericSchema]:
        return CIMultiDict(self.visit_multi_dict(schema, **kwargs))
