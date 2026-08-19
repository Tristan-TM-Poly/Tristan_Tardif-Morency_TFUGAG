import json
import tempfile
import unittest
from pathlib import Path

from src.tfuga_airgap import DCTStatus, KnowledgeAtom, classify_atom, write_review_packet, demo_atom


class TestTFUGAAirGap(unittest.TestCase):
    def test_demo_atom_passes_oak(self):
        atom = demo_atom()
        self.assertEqual(atom.status, DCTStatus.CRYSTALLIZABLE)
        self.assertTrue(atom.oak_passes())
        self.assertEqual(atom.risk_flags(), [])

    def test_overclaim_is_flagged(self):
        atom = KnowledgeAtom(
            title="Overclaim example",
            claim="This is a universal proof with guaranteed final truth.",
            status=DCTStatus.EXPLORATORY,
            assumptions=["Example assumption"],
            evidence=[],
            limitations=["Example limitation"],
            next_action="Reduce the claim and define a test.",
        )
        flags = atom.risk_flags()
        self.assertFalse(atom.oak_passes())
        self.assertTrue(any(flag.startswith("overclaim") for flag in flags))

    def test_promoted_atom_requires_evidence(self):
        atom = KnowledgeAtom(
            title="Unsupported promoted claim",
            claim="A strong result is promoted without evidence.",
            status=DCTStatus.DEMONSTRATED,
            assumptions=["Example assumption"],
            evidence=[],
            limitations=["Example limitation"],
            next_action="Add proof or downgrade status.",
        )
        self.assertIn("promotion_without_evidence", atom.risk_flags())

    def test_markdown_contains_review_sections(self):
        text = demo_atom().to_markdown()
        self.assertIn("## Claim", text)
        self.assertIn("## Assumptions", text)
        self.assertIn("## Evidence", text)
        self.assertIn("## Limitations", text)
        self.assertIn("## Next action", text)

    def test_write_review_packet(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "packet.json"
            result = write_review_packet(demo_atom(), path)
            self.assertTrue(result.exists())
            data = json.loads(result.read_text(encoding="utf-8"))
            self.assertTrue(data["oak_passes"])
            self.assertEqual(data["atom"]["status"], "X")

    def test_classify_atom_shape(self):
        packet = classify_atom(demo_atom())
        self.assertIn("timestamp", packet)
        self.assertIn("atom", packet)
        self.assertIn("risk_flags", packet)
        self.assertIn("oak_passes", packet)


if __name__ == "__main__":
    unittest.main()
