"""TFUGAG Omega Evolution Engine.

Temporal layer for OmegaGraph. It records how OmegaNodes evolve across time:
creation, revision, promotion, demotion, split, merge, quarantine and archive.
It is append-only and review-oriented; it does not mutate canon directly.
"""
from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

class OmegaEvolutionType(str, Enum):
    CREATED = "created"
    REVISED = "revised"
    PROMOTED = "promoted"
    DEMOTED = "demoted"
    SPLIT = "split"
    MERGED = "merged"
    QUARANTINED = "quarantined"
    ARCHIVED = "archived"

@dataclass(frozen=True)
class OmegaEvolutionEvent:
    event_id: str
    node_id: str
    event_type: OmegaEvolutionType
    before_state: str
    after_state: str
    reason: str
    evidence_refs: list[str]
    reviewer: str = "pending_review"

@dataclass(frozen=True)
class OmegaTrajectory:
    node_id: str
    events: list[OmegaEvolutionEvent]


def build_trajectory(node_id: str, events: list[OmegaEvolutionEvent]) -> OmegaTrajectory:
    ordered = [event for event in events if event.node_id == node_id]
    ordered = sorted(ordered, key=lambda event: event.event_id)
    return OmegaTrajectory(node_id=node_id, events=ordered)


def write_evolution_events(events: list[OmegaEvolutionEvent], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(event) for event in events], indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def write_trajectory(trajectory: OmegaTrajectory, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(trajectory), indent=2, ensure_ascii=False), encoding="utf-8")
    return path
