"""TFUGAG Omega Promotion Engine.

Promotion logic for OmegaNode maturity. It emits reviewable promotion packets
instead of modifying canon directly.
"""
from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

from src.tfuga_omega_graph import OmegaNode, OmegaNodeKind

class OmegaPromotionDecision(str, Enum):
    HOLD = "hold"
    READY_FOR_REVIEW = "ready_for_review"
    NEEDS_EVIDENCE = "needs_evidence"
    NEEDS_FRONTIER_WORK = "needs_frontier_work"
    NEEDS_OAK_REVIEW = "needs_oak_review"

@dataclass(frozen=True)
class OmegaPromotionPacket:
    node_id: str
    kind: str
    current_status: str
    decision: OmegaPromotionDecision
    target_status: str | None
    score: int
    rationale: list[str]


def evaluate_omega_promotion(node: OmegaNode) -> OmegaPromotionPacket:
    score = 0
    rationale = []
    status = node.state.status
    flags = node.state.oak_flags or []

    if node.title.strip():
        score += 10
        rationale.append("title present")
    if node.content.strip():
        score += 20
        rationale.append("content present")
    if node.state.confidence >= 0.5:
        score += 20
        rationale.append("confidence above exploratory threshold")
    if node.state.confidence >= 0.8:
        score += 20
        rationale.append("confidence above review threshold")
    if not flags:
        score += 20
        rationale.append("no OAK flags")
    else:
        rationale.append("OAK flags present")
    if node.metadata:
        score += 10
        rationale.append("metadata present")

    if flags:
        decision = OmegaPromotionDecision.NEEDS_OAK_REVIEW
        target = None
    elif node.kind in {OmegaNodeKind.EVIDENCE, OmegaNodeKind.SOURCE} and score >= 60:
        decision = OmegaPromotionDecision.READY_FOR_REVIEW
        target = "reviewed"
    elif node.kind == OmegaNodeKind.CLAIM and score >= 80:
        decision = OmegaPromotionDecision.READY_FOR_REVIEW
        target = "canonical_candidate"
    elif score < 40:
        decision = OmegaPromotionDecision.NEEDS_EVIDENCE
        target = None
    else:
        decision = OmegaPromotionDecision.HOLD
        target = None

    return OmegaPromotionPacket(
        node_id=node.node_id,
        kind=node.kind.value,
        current_status=status,
        decision=decision,
        target_status=target,
        score=score,
        rationale=rationale,
    )


def write_omega_promotion_packets(packets: list[OmegaPromotionPacket], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(packet) for packet in packets], indent=2, ensure_ascii=False), encoding="utf-8")
    return path
