from unittest.mock import sentinel

from baby_steps import given, then, when
from district42 import schema
from pytest import raises
from revolt import substitute
from revolt.errors import SubstitutionError

from district42_exp_types.multi_dict import schema_multi_dict


def test_multi_dict_substitution():
    with given:
        sch = schema_multi_dict

    with when:
        res = substitute(sch, {})

    with then:
        assert res == schema_multi_dict({})
        assert res != sch


def test_multi_dict_invalid_value_substitution_error():
    with given:
        sch = schema_multi_dict

    with when, raises(Exception) as exception:
        substitute(sch, None)

    with then:
        assert exception.type is SubstitutionError


def test_multi_dict_keys_substitution():
    with given:
        sch = schema_multi_dict
        value = {
            "id": 1,
            "name": "Bob"
        }

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema_multi_dict([
            ("id", schema.int(1)),
            ("name", schema.str("Bob")),
        ])
        assert res != sch


def test_multi_dict_multi_keys_substitution():
    with given:
        sch = schema_multi_dict
        value = [
            ("id", 1),
            ("id", "1"),
            ("name", "Bob"),
        ]

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema_multi_dict([
            ("id", schema.int(1)),
            ("id", schema.str("1")),
            ("name", schema.str("Bob")),
        ])
        assert res != sch


def test_multi_dict_value_substitution_error():
    with given:
        sch = schema_multi_dict

    with when, raises(Exception) as exception:
        substitute(sch, {"val": sentinel})

    with then:
        assert exception.type is SubstitutionError


def test_multi_dict_values_substitution():
    with given:
        sch = schema_multi_dict([
            ("id", schema.int),
            ("name", schema.str),
        ])

    with when:
        res = substitute(sch, [
            ("id", 1),
            ("name", "Bob"),
        ])

    with then:
        assert res == schema_multi_dict([
            ("id", schema.int(1)),
            ("name", schema.str("Bob")),
        ])
        assert res != sch


def test_multi_dict_list_multi_values_substitution():
    with given:
        sch = schema_multi_dict([
            ("id", schema.int),
            ("id", schema.str),
            ("name", schema.str),
        ])

    with when:
        res = substitute(sch, [
            ("id", 1),
            ("id", "1"),
            ("name", "Bob"),
        ])

    with then:
        assert res == schema_multi_dict([
            ("id", schema.int(1)),
            ("id", schema.str("1")),
            ("name", schema.str("Bob")),
        ])
        assert res != sch


def test_multi_dict_incorrect_value_substitution_error():
    with given:
        sch = schema_multi_dict({
            "id": schema.int,
        })

    with when, raises(Exception) as exception:
        substitute(sch, {"id": "1"})

    with then:
        assert exception.type is SubstitutionError


def test_multi_dict_more_keys_substitution_error():
    with given:
        sch = schema_multi_dict({
            "id": schema.int,
        })

    with when, raises(Exception) as exception:
        substitute(sch, {
            "id": 1,
            "name": "Bob",
        })

    with then:
        assert exception.type is SubstitutionError


def test_multi_dict_less_keys_substitution():
    with given:
        sch = schema_multi_dict([
            ("id", schema.int),
            ("name", schema.str),
        ])

    with when:
        res = substitute(sch, {
            "id": 1,
        })

    with then:
        assert res == schema_multi_dict([
            ("id", schema.int(1)),
            ("name", schema.str),
        ])
        assert res != sch
