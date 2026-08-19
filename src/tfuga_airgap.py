"""Minimal OAK Air-Gap kernel for TFUGAG.

This module is conservative. It does not publish externally, does not call
network APIs, and does not claim to validate scientific truth. It classifies
research artifacts so they can be reviewed before promotion.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from enum import Enum
import json
from pathlib import Path
from typing import Iterable


class DCTStatus(str, Enum):
    SPECULATIVE = "S"
    EXPLORATORY = "E"
    CRYSTALLIZABLE = "X"
    DEMONSTRATED = "D"
    CANONICAL = "C"
    ARCHIVED = "A"


@dataclass(frozen=True)
class KnowledgeAtom:
    title: str
    claim: str
    status: DCTStatus
    assumptions: list[str]
    evidence: list[str]
    limitations: list[str]
    next_action: str

    def risk_flags(self) -> list[str]:
        flags: list[str] = []
        claim_lower = self.claim.lower()
        cautious_terms = [
            "absolute proof",
            "universal proof",
            "guaranteed",
            "infinite",
            "final truth",
            "no review needed",
        ]
        for term in cautious_terms:
            if term in claim_lower:
                flags.append(f"overclaim:{term}")
        if self.status in {DCTStatus.DEMONSTRATED, DCTStatus.CANONICAL} and not self.evidence:
            flags.append("promotion_without_evidence")
        if not self.limitations:
            flags.append("missing_limitations")
        if not self.next_action.strip():
            flags.append("missing_next_action")
        return flags

    def oak_passes(self) -> bool:
        return len(self.risk_flags()) == 0

    def to_markdown(self) -> str:
        def bullets(items: Iterable[str]) -> str:
            return "\n".join(f"- {item}" for item in items) if items else "- None supplied"

        return "\n".join(
            [
                f"# {self.title}",
                "",
                f"Status: `{self.status.value}`",
                "",
                "## Claim",
                self.claim,
                "",
                "## Assumptions",
                bullets(self.assumptions),
                "",
                "## Evidence",
                bullets(self.evidence),
                "",
                "## Limitations",
                bullets(self.limitations),
                "",
                "## Next action",
                self.next_action,
                "",
                "## OAK risk flags",
                bullets(self.risk_flags()),
                "",
            ]
        )


def classify_atom(atom: KnowledgeAtom) -> dict:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "atom": asdict(atom),
        "risk_flags": atom.risk_flags(),
        "oak_passes": atom.oak_passes(),
    }


def write_review_packet(atom: KnowledgeAtom, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(classify_atom(atom), indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def demo_atom() -> KnowledgeAtom:
    return KnowledgeAtom(
        title="OAK Air-Gap governance kernel",
        claim="AI-generated TFUGAG artifacts can be classified before promotion into public canon.",
        status=DCTStatus.CRYSTALLIZABLE,
        assumptions=[
            "Artifacts are represented as bounded Knowledge Atoms.",
            "Promotion requires evidence, assumptions, limitations, and next action.",
            "Human review remains required before canonization.",
        ],
        evidence=[
            "This module produces deterministic risk flags for a minimal atom schema.",
            "Unit tests cover safe and unsafe promotion cases.",
        ],
        limitations=[
            "This is governance logic, not scientific proof validation.",
            "It does not call external APIs.",
        ],
        next_action="Add examples and expand risk rules using reviewed repository artifacts.",
    )


if __name__ == "__main__":
    output = write_review_packet(demo_atom(), "reports/oak_airgap_demo_packet.json")
    print(f"Wrote {output}")
