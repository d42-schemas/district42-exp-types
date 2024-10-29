from baby_steps import given, then, when
from d42 import schema
from d42.generation import generate
from multidict import MultiDict

from district42_exp_types.multi_dict import schema_multi_dict


def test_multi_dict_empty_generation():
    with given:
        sch = schema_multi_dict

    with when:
        res = generate(sch)

    with then:
        assert isinstance(res, MultiDict)


def test_multi_dict_generation():
    with given:
        sch = schema_multi_dict([
            ("key", schema.str("banana")),
            ("key", schema.int(42)),
        ])

    with when:
        res = generate(sch)

    with then:
        assert res == MultiDict([
            ("key", "banana"),
            ("key", 42),
        ])
