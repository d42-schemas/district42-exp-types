from district42 import register_type

from ._multidict_generator import MultiDictGenerator
from ._multidict_representor import MultiDictRepresentor
from ._multidict_schema import MultiDictProps, MultiDictSchema
from ._multidict_substitutor import MultiDictSubstitutor, MultiDictSubstitutorValidator
from ._multidict_validator import MultiDictValidator

schema_multi_dict = register_type("multi_dict", MultiDictSchema)

__all__ = ("MultiDictSchema", "schema_multi_dict", "MultiDictProps", "MultiDictRepresentor",
           "MultiDictValidator", "MultiDictSubstitutor", "MultiDictGenerator",
           "MultiDictSubstitutorValidator",)
