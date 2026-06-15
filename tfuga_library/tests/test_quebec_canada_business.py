from tfuga.quebec_canada_business import AITQuebecCanadaBusinessManager, CompanyQC, GateStatus, demo_company


def test_quebec_canada_business_manager():
    manager = AITQuebecCanadaBusinessManager()
    gates = manager.gates(demo_company())
    assert any(g.status == GateStatus.BLOCK for g in gates)
    ready = CompanyQC("ReadyCo", "corporation", True, True, True, True, True, True)
    assert manager.oak_score(manager.gates(ready)) > manager.oak_score(gates)
    assert manager.funding_routes()[0].fit_score >= manager.funding_routes()[-1].fit_score
    assert "qc_ca_oak_pipeline" in manager.markdown(demo_company())
