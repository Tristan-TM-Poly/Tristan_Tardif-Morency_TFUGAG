from tfuga import TFUGAEngine


def test_engine():
    assert TFUGAEngine().run()["tests"] == "6 passed"
