from tfuga.jkd_zero_touch import JKDZeroTouchPact


def test_pact_values():
    pact = JKDZeroTouchPact()
    assert pact.mode
    assert "GitHub" in pact.invariant
    assert pact.rules()
