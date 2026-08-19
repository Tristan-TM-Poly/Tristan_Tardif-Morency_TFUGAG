from tfuga.omniall import AITOmniAll, OmniAtom


def test_omniall_circle_power():
    layers = AITOmniAll().circle_power(3)
    assert len(layers) == 3
    assert layers[0].name == "AIT-OmniAll^o1"
    assert layers[1].name == "AIT-OmniAll^o2"


def test_omniall_rejects_empty():
    try:
        AITOmniAll().compose_once((), 1)
    except ValueError:
        assert True
    else:
        assert False


def test_omniall_lift():
    engine = AITOmniAll()
    layer = engine.compose_once((OmniAtom("x", "f", "c", 9.0, 0.1),), 1)
    atom = engine.lift(layer)
    assert atom.family == "omniall"
    assert atom.readiness >= layer.score
