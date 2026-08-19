"""TFUGAG Omega Evidence Engine.

Connects protocol candidates, observations, evidence, confidence updates and
claims. This module creates reviewable evidence packets only. It does not fetch
sources, browse the web, execute protocols, call external systems, or mutate
canon.
"""
from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

class EvidenceDirection(str, Enum):
    SUPPORTS = "supports"
    REFUTES = "refutes"
    QUALIFIES = "qualifies"
    INCONCLUSIVE = "inconclusive"

@dataclass(frozen=True)
class OmegaObservation:
    observation_id: str
    source_ref: str
    summary: str
    method_ref: str
    limitations: list[str]

@dataclass(frozen=True)
class OmegaEvidencePacket:
    evidence_id: str
    claim_ref: str
    observation_refs: list[str]
    direction: EvidenceDirection
    confidence_delta: float
    rationale: str
    review_notes: list[str]

@dataclass(frozen=True)
class OmegaConfidenceUpdate:
    claim_ref: str
    previous_confidence: float
    delta: float
    updated_confidence: float
    evidence_ref: str


def build_confidence_update(packet: OmegaEvidencePacket, previous_confidence: float) -> OmegaConfidenceUpdate:
    updated = max(0.0, min(1.0, previous_confidence + packet.confidence_delta))
    return OmegaConfidenceUpdate(
        claim_ref=packet.claim_ref,
        previous_confidence=previous_confidence,
        delta=packet.confidence_delta,
        updated_confidence=updated,
        evidence_ref=packet.evidence_id,
    )


def evidence_review_route(packet: OmegaEvidencePacket) -> str:
    if packet.direction == EvidenceDirection.REFUTES:
        return "OmegaContradiction -> OmegaMemoryPolarity -> OmegaEvolution"
    if packet.direction == EvidenceDirection.SUPPORTS:
        return "OmegaPromotion -> OmegaEvolution -> OmegaAtlas"
    if packet.direction == EvidenceDirection.QUALIFIES:
        return "OmegaPromotion Review -> OmegaAtlas"
    return "OmegaQuestion -> OmegaResearchPlanner"


def write_evidence_packets(packets: list[OmegaEvidencePacket], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(packet) for packet in packets], indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def write_confidence_updates(updates: list[OmegaConfidenceUpdate], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(update) for update in updates], indent=2, ensure_ascii=False), encoding="utf-8")
    return path
