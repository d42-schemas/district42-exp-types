from baby_steps import given, then, when
from d42 import schema, validate
from d42.validation.errors import ExtraKeyValidationError, MissingKeyValidationError
from th import PathHolder

from district42_exp_types.multi_dict import schema_multi_dict


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
