from tfuga.sedenionic import Sedenion, associator, known_zero_divisor_pair, norm_defect


def test_sedenionic_zero_divisor_and_associator():
    x, y = known_zero_divisor_pair()
    assert not x.is_zero()
    assert not y.is_zero()
    assert (x * y).is_zero()
    assert norm_defect(x, y) < 0
    assert not associator(Sedenion.basis(1), Sedenion.basis(2), Sedenion.basis(8)).is_zero()
