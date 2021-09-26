from copy import deepcopy
from typing import Any, List, Mapping

from district42 import GenericSchema
from multidict import MultiDict
from niltype import Nil, Nilable
from revolt import Substitutor, SubstitutorValidator
from revolt.errors import SubstitutionError, make_substitution_error
from th import PathHolder
from valera import ValidationResult
from valera.errors import ExtraKeyValidationError, TypeValidationError, ValidationError

from ._multi_dict_schema import MultiDictSchema

__all__ = ("MultiDictSubstitutor", "MultiDictSubstitutorValidator",)


class MultiDictSubstitutor(Substitutor, extend=True):
    def visit_multi_dict(self, schema: MultiDictSchema, *,
                         value: Any = Nil, **kwargs: Any) -> MultiDictSchema:
        if not isinstance(value, MultiDict):
            try:
                value = MultiDict(value)
            except Exception as e:
                message = f"Can't substitute to MultiDict: {e}"
                raise SubstitutionError(message)

        result = schema.__accept__(self._validator, value=value)
        if result.has_errors():
            raise make_substitution_error(result, self._formatter)

        keys = MultiDict[GenericSchema]()
        if schema.props.keys is Nil:
            for key, val in value.items():
                keys.add(key, self._from_native(val))
        else:
            for key in set(schema.props.keys):
                if key not in value:
                    for val in schema.props.keys.getall(key):
                        keys.add(key, val)
                    continue
                values = schema.props.keys.getall(key)
                candidates = value.getall(key)
                for candidate in candidates:
                    substituted = False
                    for idx, val in enumerate(values):
                        try:
                            sch = val.__accept__(self, value=candidate, **kwargs)
                        except SubstitutionError:
                            pass
                        else:
                            values[idx] = sch
                            substituted = True
                    if not substituted:
                        raise SubstitutionError(f"Can't substitute {candidate!r}")
                for val in values:
                    keys.add(key, val)

            for key, val in value.items():
                if key not in schema.props.keys:
                    raise SubstitutionError(f"Unknown key {key!r}")

        return schema.__class__(schema.props.update(keys=keys))


class MultiDictSubstitutorValidator(SubstitutorValidator, extend=True):
    def __validate_candidates(self, value: GenericSchema, path: PathHolder,
                              candidates: List[Any], **kwargs: Any) -> List[ValidationError]:
        all_errors = []
        for candidate in candidates:
            res = value.__accept__(self, value=candidate, path=path, **kwargs)
            if not res.has_errors():
                return []
            all_errors.append(res.get_errors())
        all_errors.sort(key=len)
        return all_errors[0]

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

        for key in set(schema.props.keys):
            if key not in value:
                continue

            nested_path = deepcopy(path)[key]
            if isinstance(value, MultiDict):
                candidates = value.getall(key)
                for val in schema.props.keys.getall(key):
                    errors = self.__validate_candidates(val, nested_path, candidates, **kwargs)
                    result.add_errors(errors)
            else:
                val = schema.props.keys.getone(key)
                res = val.__accept__(self, value=value[key], path=nested_path, **kwargs)
                result.add_errors(res.get_errors())

        for key in set(value):
            if key not in schema.props.keys:
                result.add_error(ExtraKeyValidationError(path, value, key))
            else:
                vals = value.getall(key) if isinstance(value, MultiDict) else [value.get(key)]
                if len(vals) > len(schema.props.keys.getall(key)):
                    result.add_error(ExtraKeyValidationError(path, value, key))

        return result
