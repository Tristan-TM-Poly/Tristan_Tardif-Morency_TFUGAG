"""TFUGAG Agent Bridge blueprint.

This file defines a safe boundary for connecting an external model service to
repository work. It does not contain credentials and does not perform network
calls by default.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path


class ActionType(str, Enum):
    CREATE_ATOM = "create_atom"
    CREATE_REPORT = "create_report"
    SUGGEST_CODE = "suggest_code"
    OPEN_REVIEW = "open_review"


@dataclass(frozen=True)
class AgentAction:
    action_type: ActionType
    title: str
    rationale: str
    target_path: str
    content: str

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.title.strip():
            issues.append("missing_title")
        if not self.rationale.strip():
            issues.append("missing_rationale")
        if not self.target_path.strip():
            issues.append("missing_target_path")
        if self.target_path.startswith("/") or ".." in Path(self.target_path).parts:
            issues.append("unsafe_target_path")
        if not self.content.strip():
            issues.append("missing_content")
        return issues

    def is_safe(self) -> bool:
        return not self.validate()


def build_review_payload(action: AgentAction) -> dict:
    return {
        "action": asdict(action),
        "issues": action.validate(),
        "safe_to_stage": action.is_safe(),
        "review_rule": "stage on a branch and require review before merge",
    }


def write_action_review(action: AgentAction, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_review_payload(action), indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def system_prompt() -> str:
    return """You are the TFUGAG external research assistant.
You may propose Knowledge Atoms, reports, tests, and code patches.
You must not include credentials, secrets, private data, or unsupported claims.
Every external action must be staged for review before becoming canonical.
For each output, provide: title, rationale, target_path, content, assumptions, limitations, and next action.
"""
