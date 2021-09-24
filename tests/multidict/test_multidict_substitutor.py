from baby_steps import given, then, when
from revolt import substitute

from district42_exp_types.multidict import schema_multi_dict


def test_multi_dict_substitution():
    with given:
        sch = schema_multi_dict

    with when:
        res = substitute(sch, {})

    with then:
        assert res == schema_multi_dict({})
        assert res != sch
