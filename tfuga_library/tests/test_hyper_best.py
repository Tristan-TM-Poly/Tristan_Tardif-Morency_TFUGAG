from tfuga.hyper_best import TFUGAHyperBest


def test_hyper_best_rank_and_markdown():
    kernel = TFUGAHyperBest()
    ranked = kernel.rank()
    assert ranked
    assert ranked[0].score >= ranked[-1].score
    assert "composition_only" in kernel.markdown()
