"""OAK Quarantine layer for TFUGAG.

Quarantine does not delete or rewrite atoms. It creates review packets when a
claim conflict, missing evidence, missing limitation, or other integrity issue
requires arbitration before canon promotion.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

from src.tfuga_agent_bridge import ActionType, AgentAction
from src.tfuga_contradiction_engine import ContradictionCandidate


class QuarantineReason(str, Enum):
    CONTRADICTION = "contradiction"
    MISSING_EVIDENCE = "missing_evidence"
    MISSING_LIMITATION = "missing_limitation"
    OVERCLAIM = "overclaim"
    REVIEW_REQUIRED = "review_required"


@dataclass(frozen=True)
class QuarantinePacket:
    packet_id: str
    reason: QuarantineReason
    affected_ids: list[str]
    rationale: str
    evidence_needed: list[str]
    recommended_next_action: str

    def to_agent_action(self) -> AgentAction:
        return AgentAction(
            action_type=ActionType.OPEN_REVIEW,
            title=f"OAK quarantine: {self.reason.value}",
            rationale=self.rationale,
            target_path=f"reviews/quarantine/{self.packet_id}.json",
            content=json.dumps(asdict(self), indent=2, ensure_ascii=False),
        )


def packet_from_contradiction(candidate: ContradictionCandidate) -> QuarantinePacket:
    packet_id = f"{candidate.left_id}__{candidate.right_id}"
    return QuarantinePacket(
        packet_id=packet_id,
        reason=QuarantineReason.CONTRADICTION,
        affected_ids=[candidate.left_id, candidate.right_id],
        rationale=candidate.rationale,
        evidence_needed=[
            "State each claim in minimal form.",
            "List assumptions for each affected atom.",
            "Provide a decisive counterexample, proof, calculation, or experiment.",
        ],
        recommended_next_action="Open an arbitration review before either atom is promoted.",
    )


def write_quarantine_packet(packet: QuarantinePacket, output_dir: str | Path = "reviews/quarantine") -> Path:
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{packet.packet_id}.json"
    path.write_text(json.dumps(asdict(packet), indent=2, ensure_ascii=False), encoding="utf-8")
    return path
