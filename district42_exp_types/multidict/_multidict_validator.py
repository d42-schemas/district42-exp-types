from copy import deepcopy
from typing import Any, Mapping

from multidict import MultiDict
from niltype import Nil, Nilable
from th import PathHolder
from valera import ValidationResult, Validator
from valera.errors import ExtraKeyValidationError, MissingKeyValidationError, TypeValidationError

from ._multidict_schema import MultiDictSchema

__all__ = ("MultiDictValidator",)


class MultiDictValidator(Validator, extend=True):
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
            if key not in value:
                result.add_error(MissingKeyValidationError(path, value, key))
                continue

            nested_path = deepcopy(path)[key]
            if isinstance(value, MultiDict):
                all_errors = []
                candidates = value.getall(key)
                for candidate in candidates:
                    res = val.__accept__(self, value=candidate, path=nested_path, **kwargs)
                    all_errors.append(res.get_errors())
                all_errors.sort(key=len)
                result.add_errors(all_errors[0])
            else:
                res = val.__accept__(self, value=value[key], path=nested_path, **kwargs)
                result.add_errors(res.get_errors())

        if len(schema.props.keys) != len(value):
            for key, val in value.items():
                if key not in schema.props.keys:
                    result.add_error(ExtraKeyValidationError(path, value, key))

        return result
