from tfuga import AITAutonomousGenesis, GenesisPolicy, GenesisSeed


def test_genesis_accepts_good_low_risk_seed():
    engine = AITAutonomousGenesis()
    report = engine.generate([GenesisSeed("demo", "build useful module", "test", 4.0, "low")])
    assert len(report.accepted) == 1
    assert "AIT Autonomous Genesis Report" in report.markdown


def test_genesis_rejects_high_risk_by_default():
    engine = AITAutonomousGenesis()
    report = engine.generate([GenesisSeed("danger", "unsafe autonomy", "test", 5.0, "high")])
    assert len(report.rejected) == 1


def test_genesis_policy_can_raise_threshold():
    engine = AITAutonomousGenesis(GenesisPolicy(min_oak_score=9.5))
    report = engine.generate([GenesisSeed("small", "minor gain", "test", 1.0, "low")])
    assert len(report.accepted) == 0


def test_default_seeds_generate_multiple_proposals():
    engine = AITAutonomousGenesis()
    report = engine.generate(engine.default_seeds())
    assert len(report.proposals) == 3
    assert len(report.accepted) >= 1
