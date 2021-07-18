from typing import Any
from uuid import UUID

from niltype import Nil, Nilable
from th import PathHolder
from valera import ValidationResult, Validator
from valera.errors import TypeValidationError, ValidationError, ValueValidationError

from ._uuid_str_schema import UUIDStrSchema

__all__ = ("UUIDStrValidator", "StrCaseValidationError",)


class StrCaseValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: str, expected_case: str) -> None:
        self._path = path
        self._actual_value = actual_value
        self._expected_case = expected_case

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self._path!r}, {self._actual_value!r}, "
                f"{self._expected_case!r})")


class UUIDStrValidator(Validator, extend=True):
    def visit_uuid_str(self, schema: UUIDStrSchema, *,
                       value: Any = Nil, path: Nilable[PathHolder] = Nil,
                       **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if error := self._validate_type(path, value, str):
            return result.add_error(error)

        try:
            actual_value = UUID(value)
        except (TypeError, ValueError):
            if schema.props.value is not Nil:
                error = ValueValidationError(path, value, schema.props.value)
            else:
                error = TypeValidationError(path, value, UUID)
            return result.add_error(error)

        if schema.props.value is not Nil:
            if actual_value != UUID(schema.props.value):
                error = ValueValidationError(path, value, schema.props.value)
                return result.add_error(error)

        if schema.props.is_lowercase is not Nil:
            if not value.islower():
                error = StrCaseValidationError(path, value, str.lower.__name__)
                return result.add_error(error)

        if schema.props.is_uppercase is not Nil:
            if not value.isupper():
                error = StrCaseValidationError(path, value, str.upper.__name__)
                return result.add_error(error)

        return result
