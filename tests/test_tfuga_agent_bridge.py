import json
import tempfile
import unittest
from pathlib import Path

from src.tfuga_agent_bridge import ActionType, AgentAction, build_review_payload, system_prompt, write_action_review


class TestTFUGAAgentBridge(unittest.TestCase):
    def test_valid_action_is_safe(self):
        action = AgentAction(
            action_type=ActionType.CREATE_ATOM,
            title="Create atom",
            rationale="Capture a bounded research idea.",
            target_path="knowledge_atoms/example.md",
            content="# Example\n",
        )
        self.assertTrue(action.is_safe())
        self.assertEqual(action.validate(), [])

    def test_empty_fields_are_flagged(self):
        action = AgentAction(
            action_type=ActionType.CREATE_REPORT,
            title="",
            rationale="",
            target_path="",
            content="",
        )
        self.assertFalse(action.is_safe())
        self.assertIn("missing_title", action.validate())
        self.assertIn("missing_rationale", action.validate())
        self.assertIn("missing_target_path", action.validate())
        self.assertIn("missing_content", action.validate())

    def test_unsafe_path_is_flagged(self):
        action = AgentAction(
            action_type=ActionType.SUGGEST_CODE,
            title="Bad path",
            rationale="Test path validation.",
            target_path="../secret.txt",
            content="nope",
        )
        self.assertIn("unsafe_target_path", action.validate())

    def test_payload_shape(self):
        action = AgentAction(
            action_type=ActionType.OPEN_REVIEW,
            title="Review",
            rationale="Prepare a review packet.",
            target_path="reports/review.json",
            content="{}",
        )
        payload = build_review_payload(action)
        self.assertTrue(payload["safe_to_stage"])
        self.assertIn("review_rule", payload)

    def test_write_action_review(self):
        action = AgentAction(
            action_type=ActionType.CREATE_REPORT,
            title="Report",
            rationale="Write a local report.",
            target_path="reports/report.md",
            content="Report body",
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = write_action_review(action, Path(tmp) / "action.json")
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(data["safe_to_stage"])

    def test_system_prompt_contains_review_boundary(self):
        prompt = system_prompt().lower()
        self.assertIn("review", prompt)
        self.assertIn("credentials", prompt)


if __name__ == "__main__":
    unittest.main()
