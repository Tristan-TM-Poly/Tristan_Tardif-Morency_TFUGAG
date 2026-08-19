import json
import tempfile
import unittest
from pathlib import Path

from src.tfuga_airgap import DCTStatus, KnowledgeAtom
from src.tfuga_preventive_generator import (
    FocusType,
    PreventiveLens,
    ZoomFocus,
    atom_to_focus,
    generate_preventive_seeds,
    proposals_for_zoom,
    review_questions_for_lens,
    write_preventive_subgraph,
)


class TestPreventiveGenerator(unittest.TestCase):
    def test_generates_all_lenses(self):
        focus = ZoomFocus("tfuga", "TFUGA", FocusType.THEORY, "Knowledge evolution architecture")
        seeds = generate_preventive_seeds(focus)
        self.assertEqual(len(seeds), len(PreventiveLens))
        self.assertEqual({seed.lens for seed in seeds}, set(PreventiveLens))

    def test_each_lens_has_questions(self):
        for lens in PreventiveLens:
            self.assertGreater(len(review_questions_for_lens(lens)), 0)

    def test_seeds_convert_to_safe_proposals(self):
        focus = ZoomFocus("app", "Application", FocusType.APPLICATION, "Potential use case")
        proposals = proposals_for_zoom(focus)
        self.assertEqual(len(proposals), len(PreventiveLens))
        self.assertTrue(all(proposal.action.is_safe() for proposal in proposals))

    def test_atom_to_focus(self):
        atom = KnowledgeAtom(
            title="Raman baseline correction",
            claim="Baseline correction can improve Raman spectrum interpretation.",
            status=DCTStatus.EXPLORATORY,
            assumptions=["spectra contain background drift"],
            evidence=[],
            limitations=["method-dependent"],
            next_action="compare methods",
        )
        focus = atom_to_focus("atom-1", atom, FocusType.APPLICATION)
        self.assertEqual(focus.focus_id, "atom-1")
        self.assertEqual(focus.title, atom.title)
        self.assertEqual(focus.focus_type, FocusType.APPLICATION)

    def test_write_preventive_subgraph(self):
        focus = ZoomFocus("sys", "System", FocusType.SYSTEM, "A bounded system")
        with tempfile.TemporaryDirectory() as tmp:
            path = write_preventive_subgraph(focus, Path(tmp) / "preventive.json")
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(len(data), len(PreventiveLens))


if __name__ == "__main__":
    unittest.main()
