"""TFUGAG Omega Contradiction Engine.

Creates reviewable conflict packets from incompatible claims, refuting evidence,
or high contradiction pressure. It does not prove logical inconsistency by
itself, execute solvers, call external systems, or mutate canon.
"""
from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

class ContradictionSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ConflictDecision(str, Enum):
    MONITOR = "monitor"
    REVIEW = "review"
    QUARANTINE = "quarantine"
    ARCHIVE_CANDIDATE = "archive_candidate"

@dataclass(frozen=True)
class OmegaConflictPacket:
    conflict_id: str
    claim_a_ref: str
    claim_b_ref: str | None
    evidence_refs: list[str]
    conflict_statement: str
    assumptions: list[str]
    severity: ContradictionSeverity
    decision: ConflictDecision
    review_route: str


def classify_conflict(evidence_count: int, assumption_count: int, has_direct_refutation: bool) -> tuple[ContradictionSeverity, ConflictDecision]:
    if has_direct_refutation and evidence_count >= 2:
        return ContradictionSeverity.CRITICAL, ConflictDecision.QUARANTINE
    if has_direct_refutation:
        return ContradictionSeverity.HIGH, ConflictDecision.REVIEW
    if evidence_count >= 2 and assumption_count <= 1:
        return ContradictionSeverity.MEDIUM, ConflictDecision.REVIEW
    return ContradictionSeverity.LOW, ConflictDecision.MONITOR


def build_conflict_packet(
    conflict_id: str,
    claim_a_ref: str,
    conflict_statement: str,
    evidence_refs: list[str],
    assumptions: list[str],
    claim_b_ref: str | None = None,
    has_direct_refutation: bool = False,
) -> OmegaConflictPacket:
    severity, decision = classify_conflict(len(evidence_refs), len(assumptions), has_direct_refutation)
    if decision == ConflictDecision.QUARANTINE:
        route = "OmegaMemoryPolarity -> OmegaEvolution -> OAK Review"
    elif decision == ConflictDecision.REVIEW:
        route = "OmegaEvidence -> OmegaPromotion Review -> OmegaAtlas"
    else:
        route = "OmegaKernel monitor"
    return OmegaConflictPacket(
        conflict_id=conflict_id,
        claim_a_ref=claim_a_ref,
        claim_b_ref=claim_b_ref,
        evidence_refs=evidence_refs,
        conflict_statement=conflict_statement,
        assumptions=assumptions,
        severity=severity,
        decision=decision,
        review_route=route,
    )


def write_conflict_packets(packets: list[OmegaConflictPacket], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(packet) for packet in packets], indent=2, ensure_ascii=False), encoding="utf-8")
    return path
