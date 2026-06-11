import unittest

from src.tfuga_airgap import DCTStatus, KnowledgeAtom
from src.tfuga_bridge_engine import cosine_similarity, propose_bridge, propose_bridges, term_vector
from src.tfuga_graph import RelationType


def atom(title, claim):
    return KnowledgeAtom(
        title=title,
        claim=claim,
        status=DCTStatus.EXPLORATORY,
        assumptions=["bounded review"],
        evidence=[],
        limitations=["draft"],
        next_action="review",
    )


class TestTFUGABridgeEngine(unittest.TestCase):
    def test_cosine_similarity_identical_vectors(self):
        vector = term_vector("oscillator energy resonance")
        self.assertAlmostEqual(cosine_similarity(vector, vector), 1.0)

    def test_cosine_similarity_empty_vector(self):
        self.assertEqual(cosine_similarity(term_vector(""), term_vector("abc")), 0.0)

    def test_propose_bridge_above_threshold(self):
        left = atom("LC circuit", "An LC circuit stores energy in oscillating electric and magnetic fields.")
        right = atom("harmonic oscillator", "A harmonic oscillator stores energy through oscillating position and momentum.")
        candidate = propose_bridge("a", left, "b", right, threshold=0.05)
        self.assertIsNotNone(candidate)
        self.assertEqual(candidate.relation, RelationType.ANALOGOUS_TO)

    def test_propose_bridge_rejects_self(self):
        left = atom("same", "same claim")
        self.assertIsNone(propose_bridge("a", left, "a", left))

    def test_propose_bridges_sorted(self):
        atoms = {
            "a": atom("LC circuit", "oscillator energy resonance"),
            "b": atom("Harmonic oscillator", "oscillator energy resonance"),
            "c": atom("Unrelated", "botanical leaf pigment"),
        }
        candidates = propose_bridges(atoms, threshold=0.05)
        self.assertGreaterEqual(len(candidates), 1)
        self.assertGreaterEqual(candidates[0].score, candidates[-1].score)


if __name__ == "__main__":
    unittest.main()
