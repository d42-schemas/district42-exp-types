from typing import Any, Dict, Mapping

import pytest
from baby_steps import given, then, when
from district42 import schema
from multidict import MultiDict
from th import PathHolder
from valera import validate
from valera.errors import ExtraKeyValidationError, MissingKeyValidationError, TypeValidationError

from district42_exp_types.multidict import schema_multi_dict


@pytest.mark.parametrize("value", [
    {},
    {"id": 1},
    {"id": 1, "name": "Bob"},
])
def test_multi_dict_type_validation(value: Dict[Any, Any]):
    with given:
        sch = schema_multi_dict

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == []


def test_multi_dict_type_validation_error():
    with given:
        sch = schema_multi_dict
        value = []

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            TypeValidationError(PathHolder(), value, Mapping)
        ]


def test_multi_dict_no_keys_validation():
    with given:
        sch = schema_multi_dict({})
        value = {}

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == []


def test_multi_dict_keys_validation():
    with given:
        sch = schema_multi_dict({
            "id": schema.int,
            "name": schema.str,
        })
        value = {"id": 1, "name": "Bob"}

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == []


def test_multi_dict_extra_key_validation_error():
    with given:
        sch = schema_multi_dict({})
        value = {"id": 1}

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            ExtraKeyValidationError(PathHolder(), value, "id")
        ]


def test_multi_dict_missing_key_validation_error():
    with given:
        sch = schema_multi_dict({
            "id": schema.int,
            "name": schema.str,
        })
        value = {"id": 1}

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            MissingKeyValidationError(PathHolder(), value, "name")
        ]


def test_multi_dict_nested_keys_validation():
    with given:
        sch = schema_multi_dict({
            "result": schema_multi_dict({
                "id": schema.int,
                "name": schema.str,
            })
        })
        value = {
            "result": {
                "id": 1,
                "name": "Bob"
            }
        }

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == []


def test_multi_dict_nested_extra_key_valudidation_error():
    with given:
        sch = schema_multi_dict({
            "result": schema_multi_dict({
                "id": schema.int,
            })
        })
        value = {
            "result": {
                "id": 1,
                "name": "Bob",
            }
        }

    with when:
        result = validate(sch, value)

    with then:
        path = PathHolder()["result"]
        assert result.get_errors() == [
            ExtraKeyValidationError(path, value["result"], "name")
        ]


def test_multi_dict_nested_missing_key_valudidation_error():
    with given:
        sch = schema_multi_dict({
            "result": schema_multi_dict({
                "id": schema.int,
                "name": schema.str,
            })
        })
        value = {
            "result": {
                "id": 1
            }
        }

    with when:
        result = validate(sch, value)

    with then:
        path = PathHolder()["result"]
        assert result.get_errors() == [
            MissingKeyValidationError(path, value["result"], "name")
        ]


def test_multi_dict_multidict_validation():
    with given:
        sch = schema_multi_dict([
            ("id", schema.int(42)),
            ("id", schema.str("42")),
            ("name", schema.str("Bob")),
        ])
        value = MultiDict([
            ("id", 42),
            ("id", "42"),
            ("name", "Bob"),
        ])

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == []


def test_multi_dict_multidict_extra_value_validation_error():
    with given:
        sch = schema_multi_dict([
            ("id", schema.int(42)),
            ("name", schema.str("Bob")),
        ])
        value = MultiDict([
            ("id", 42),
            ("id", "42"),
            ("name", "Bob"),
        ])

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            ExtraKeyValidationError(PathHolder(), value, "id")
        ]


def test_multi_dict_multidict_missing_value_validation_error():
    with given:
        sch = schema_multi_dict([
            ("id", schema.int(42)),
            ("id", schema.str("42")),
            ("name", schema.str("Bob")),
        ])
        value = MultiDict([
            ("id", 42),
            ("name", "Bob"),
        ])

    with when:
        result = validate(sch, value)

    with then:
        assert result.get_errors() == [
            TypeValidationError(PathHolder()['id'], 42, str)
        ]
