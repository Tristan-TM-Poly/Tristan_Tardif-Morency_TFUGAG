from tfuga.constant_atlas import TFUGAConstantAtlas


def test_constant_atlas_known_derived_unknown():
    atlas = TFUGAConstantAtlas()
    assert atlas.by_key()["c"].value == 299792458.0
    assert atlas.derived()["planck_length"] > 0
    assert atlas.unknown_slots()
    assert "known_derived_unknown_oak" in atlas.markdown()
