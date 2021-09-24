from copy import deepcopy
from typing import Any, Mapping

from district42 import GenericSchema
from multidict import MultiDict
from niltype import Nil, Nilable
from revolt import Substitutor, SubstitutorValidator
from revolt.errors import SubstitutionError, make_substitution_error
from th import PathHolder
from valera import ValidationResult
from valera.errors import ExtraKeyValidationError, TypeValidationError

from ._multidict_schema import MultiDictSchema

__all__ = ("MultiDictSubstitutor", "MultiDictSubstitutorValidator",)


class MultiDictSubstitutor(Substitutor, extend=True):
    def visit_multi_dict(self, schema: MultiDictSchema, *,
                         value: Any = Nil, **kwargs: Any) -> MultiDictSchema:
        result = schema.__accept__(self._validator, value=value)
        if result.has_errors():
            raise make_substitution_error(result, self._formatter)

        keys = MultiDict[GenericSchema]()
        if schema.props.keys is Nil:
            for key, val in value.items():
                keys.add(key, self._from_native(val))
        else:
            for key, val in schema.props.keys.items():
                if key in value:
                    keys.add(key, val.__accept__(self, value=value[key], **kwargs))
                else:
                    keys.add(key, val)
            for key, val in value.items():
                if key not in schema.props.keys:
                    raise SubstitutionError(f"Unknown key {key!r}")

        return schema.__class__(schema.props.update(keys=keys))


class MultiDictSubstitutorValidator(SubstitutorValidator, extend=True):
    def visit_multi_dict(self, schema: MultiDictSchema, *,
                         value: Any = Nil, path: Nilable[PathHolder] = Nil,
                         **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if not isinstance(value, Mapping):
            return result.add_error(TypeValidationError(path, value, Mapping))

        if schema.props.keys is Nil:
            return result

        for key, val in schema.props.keys.items():
            if key in value:
                nested_path = deepcopy(path)[key]
                res = val.__accept__(self, value=value[key], path=nested_path, **kwargs)
                result.add_errors(res.get_errors())

        if len(schema.props.keys) != len(value):
            for key, val in value.items():
                if key not in schema.props.keys:
                    result.add_error(ExtraKeyValidationError(path, value, key))

        return result
