from ait2 import AITGenerator, AITSpec
from ait2.cvcd import CVCDScorer
from ait2.hgfm import HGFMMapper


def test_generator_produces_promotable_packet():
    packet = AITGenerator().generate("create math proof agents")
    assert packet.spec.name.startswith("AIT-")
    assert packet.cvcd_score > 0
    assert packet.oak_report.status >= 2
    assert packet.oak_report.tests


def test_hgfm_records_missing_validators_as_residue():
    spec = AITSpec(
        name="AIT-NoValidators",
        mission="Test missing validators",
        inputs=["x"],
        outputs=["y"],
        tools=[],
        validators=[],
        memory_read=[],
        memory_write=[],
        yield_targets=[],
    )
    graph = HGFMMapper().map(spec)
    assert graph["residues"]


def test_cvcd_is_bounded():
    score = CVCDScorer().score({"nodes": [], "hyperedges": [], "residues": []})
    assert 0.0 <= score <= 1.0
