from baby_steps import given, then, when
from d42 import validate
from d42.validation.errors import TypeValidationError
from th import PathHolder

from district42_exp_types.sdict import schema_sdict


def test_sdict_type_validation():
    with when:
        result = validate(schema_sdict, {})

    with then:
        assert result.get_errors() == []


def test_sdict_type_validation_error():
    with given:
        value = []

    with when:
        result = validate(schema_sdict, value)

    with then:
        assert result.get_errors() == [
            TypeValidationError(PathHolder(), value, dict)
        ]
