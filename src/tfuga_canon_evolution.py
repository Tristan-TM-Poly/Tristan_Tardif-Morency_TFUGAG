"""Canon Evolution Tracker for TFUGAG.

Tracks proposed changes to atoms, claims, and canon entries without applying
those changes automatically. Every evolution is a reviewable event with a
reason, source, and before/after status.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

from src.tfuga_airgap import DCTStatus


class EvolutionEventType(str, Enum):
    CREATED = "created"
    PROMOTED = "promoted"
    DEMOTED = "demoted"
    REVISED = "revised"
    QUARANTINED = "quarantined"
    ARCHIVED = "archived"


@dataclass(frozen=True)
class CanonEvolutionEvent:
    atom_id: str
    event_type: EvolutionEventType
    previous_status: DCTStatus | None
    next_status: DCTStatus | None
    reason: str
    evidence_refs: list[str]
    reviewer: str = "pending_review"


def make_promotion_event(atom_id: str, previous: DCTStatus, next_status: DCTStatus, reason: str, evidence_refs: list[str]) -> CanonEvolutionEvent:
    return CanonEvolutionEvent(
        atom_id=atom_id,
        event_type=EvolutionEventType.PROMOTED,
        previous_status=previous,
        next_status=next_status,
        reason=reason,
        evidence_refs=evidence_refs,
    )


def make_quarantine_event(atom_id: str, status: DCTStatus, reason: str, evidence_refs: list[str]) -> CanonEvolutionEvent:
    return CanonEvolutionEvent(
        atom_id=atom_id,
        event_type=EvolutionEventType.QUARANTINED,
        previous_status=status,
        next_status=status,
        reason=reason,
        evidence_refs=evidence_refs,
    )


def write_evolution_log(events: list[CanonEvolutionEvent], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(event) for event in events], indent=2, ensure_ascii=False), encoding="utf-8")
    return path
