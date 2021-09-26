from typing import Any

from district42.representor import Representor

from ._ci_multi_dict_schema import CIMultiDictSchema

__all__ = ("CIMultiDictRepresentor",)


class CIMultiDictRepresentor(Representor, extend=True):
    def visit_ci_multi_dict(self, schema: CIMultiDictSchema, *,
                            indent: int = 0, **kwargs: Any) -> str:
        r = self.visit_multi_dict(schema, indent=indent, **kwargs)
        # dirty, but who cares
        prefix = f"{self._name}.multi_dict"
        return f"{self._name}.ci_multi_dict" + str(r[len(prefix):])
