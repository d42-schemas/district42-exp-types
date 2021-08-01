from baby_steps import then, when

from district42_exp_types.sdict import SDictSchema, schema_sdict


def test_sdict_declaration():
    with when:
        sch = schema_sdict

    with then:
        assert isinstance(sch, SDictSchema)
