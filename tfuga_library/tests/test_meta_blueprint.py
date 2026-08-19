from tfuga.meta_blueprint import AITMetaBlueprint, MetaNeed


def test_meta_blueprint_proposes_ready_plan():
    engine = AITMetaBlueprint()
    pairs = engine.propose((MetaNeed("status", "parquet absorber", "missing"),))
    assert pairs
    blueprint, readiness = pairs[0]
    assert "parquet" in blueprint.name.lower()
    assert readiness.approved
