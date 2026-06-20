from tfuga.venture_setup import AITVentureSetup


def test_venture_setup_defaults_and_markdown():
    setup = AITVentureSetup()
    plans = setup.portfolio()
    assert len(plans) >= 4
    assert plans[0].score > 0
    assert "AIT Venture Setup" in setup.markdown()
