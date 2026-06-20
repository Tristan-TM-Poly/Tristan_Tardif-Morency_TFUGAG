from tfuga.hyper_synergy import TFUGAHyperSynergy


def test_hyper_synergy_top_edges():
    engine = TFUGAHyperSynergy()
    edges = engine.top(3)
    assert edges
    assert edges[0].score >= edges[-1].score
    assert "composition_only" in engine.markdown()
