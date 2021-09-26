from typing import Any, Dict, cast

from blahblah import Generator

from ._ci_multi_dict_schema import CIMultiDictSchema

__all__ = ("CIMultiDictGenerator",)


class CIMultiDictGenerator(Generator, extend=True):
    def visit_ci_multi_dict(self, schema: CIMultiDictSchema, **kwargs: Any) -> Dict[str, Any]:
        return cast(Dict[str, Any], self.visit_multi_dict(schema, **kwargs))
