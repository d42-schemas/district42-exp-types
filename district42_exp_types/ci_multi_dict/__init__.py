from district42 import register_type

from district42_exp_types.multi_dict import schema_multi_dict

from ._ci_multi_dict_generator import CIMultiDictGenerator
from ._ci_multi_dict_representor import CIMultiDictRepresentor
from ._ci_multi_dict_schema import CIMultiDictProps, CIMultiDictSchema
from ._ci_multi_dict_substitutor import CIMultiDictSubstitutor
from ._ci_multi_dict_validator import CIMultiDictValidator

schema_ci_multi_dict = register_type("ci_multi_dict", CIMultiDictSchema)

__all__ = ("CIMultiDictSchema", "schema_ci_multi_dict", "schema_multi_dict", "CIMultiDictProps",
           "CIMultiDictRepresentor", "CIMultiDictGenerator", "CIMultiDictSubstitutor",
           "CIMultiDictValidator",)
