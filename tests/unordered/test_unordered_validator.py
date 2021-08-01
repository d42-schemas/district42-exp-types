from typing import Any, List

import pytest
from baby_steps import given, then, when
from th import PathHolder
from valera import validate
from valera.errors import TypeValidationError

from district42_exp_types.unordered import unordered_schema


@pytest.mark.parametrize("value", [
    [],
    [1],
    [1, 2],
    [42, 3.14, "banana"],
])
def test_unordered_type_validation(value: List[Any]):
    with when:
        result = validate(unordered_schema, value)

    with then:
        assert result.get_errors() == []


def test_unordered_type_validation_error():
    with given:
        value = {}

    with when:
        result = validate(unordered_schema, value)

    with then:
        assert result.get_errors() == [
            TypeValidationError(PathHolder(), value, list),
        ]
