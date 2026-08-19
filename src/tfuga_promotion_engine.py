"""Promotion Engine for TFUGAG.

This module evaluates whether a Knowledge Atom is ready for promotion. It does
not mutate the atom or the canon. It emits a promotion review packet.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

from src.tfuga_airgap import DCTStatus, KnowledgeAtom


class PromotionDecision(str, Enum):
    HOLD = "hold"
    PROMOTE_CANDIDATE = "promote_candidate"
    NEEDS_EVIDENCE = "needs_evidence"
    NEEDS_LIMITATIONS = "needs_limitations"
    NEEDS_REVIEW = "needs_review"


@dataclass(frozen=True)
class PromotionPacket:
    atom_id: str
    current_status: DCTStatus
    decision: PromotionDecision
    target_status: DCTStatus | None
    score: int
    rationale: list[str]


def evaluate_promotion(atom_id: str, atom: KnowledgeAtom) -> PromotionPacket:
    score = 0
    rationale: list[str] = []

    if atom.assumptions:
        score += 20
        rationale.append("assumptions present")
    if atom.evidence:
        score += 30
        rationale.append("evidence present")
    if atom.limitations:
        score += 20
        rationale.append("limitations present")
    if atom.next_action.strip():
        score += 10
        rationale.append("next action present")
    if atom.oak_passes():
        score += 20
        rationale.append("OAK risk flags clear")
    else:
        rationale.append("OAK risk flags require review")

    if not atom.evidence:
        return PromotionPacket(atom_id, atom.status, PromotionDecision.NEEDS_EVIDENCE, None, score, rationale)
    if not atom.limitations:
        return PromotionPacket(atom_id, atom.status, PromotionDecision.NEEDS_LIMITATIONS, None, score, rationale)
    if not atom.oak_passes():
        return PromotionPacket(atom_id, atom.status, PromotionDecision.NEEDS_REVIEW, None, score, rationale)

    if score >= 80 and atom.status in {DCTStatus.SPECULATIVE, DCTStatus.EXPLORATORY}:
        return PromotionPacket(atom_id, atom.status, PromotionDecision.PROMOTE_CANDIDATE, DCTStatus.CRYSTALLIZABLE, score, rationale)
    if score >= 90 and atom.status == DCTStatus.CRYSTALLIZABLE:
        return PromotionPacket(atom_id, atom.status, PromotionDecision.PROMOTE_CANDIDATE, DCTStatus.DEMONSTRATED, score, rationale)
    return PromotionPacket(atom_id, atom.status, PromotionDecision.HOLD, None, score, rationale)


def evaluate_all(atoms: dict[str, KnowledgeAtom]) -> list[PromotionPacket]:
    return sorted([evaluate_promotion(atom_id, atom) for atom_id, atom in atoms.items()], key=lambda packet: packet.score, reverse=True)


def write_promotion_packets(packets: list[PromotionPacket], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(packet) for packet in packets], indent=2, ensure_ascii=False), encoding="utf-8")
    return path
