from baby_steps import given, then, when
from revolt import substitute

from district42_exp_types.sdict import schema_sdict


def test_sdict_substitution():
    with given:
        sch = schema_sdict

    with when:
        res = substitute(sch, {})

    with then:
        assert res == schema_sdict({})
        assert res != sch
