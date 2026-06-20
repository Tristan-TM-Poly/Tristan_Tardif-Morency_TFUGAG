"""Frontier Detector for TFUGAG.

Detects under-connected atoms, missing evidence, missing limitations, and
potential focus zones for preventive generation. It emits observations only;
it does not mutate the graph or canon.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

from src.tfuga_airgap import KnowledgeAtom
from src.tfuga_graph import KnowledgeGraph


class FrontierType(str, Enum):
    ORPHAN_ATOM = "orphan_atom"
    LOW_EVIDENCE = "low_evidence"
    LOW_LIMITATION = "low_limitation"
    HIGH_DEGREE = "high_degree"
    REVIEW_FOCUS = "review_focus"


@dataclass(frozen=True)
class FrontierObservation:
    atom_id: str
    frontier_type: FrontierType
    score: int
    rationale: str


def graph_degree(graph: KnowledgeGraph, atom_id: str) -> int:
    return len(graph.neighbors(atom_id))


def detect_frontiers(graph: KnowledgeGraph) -> list[FrontierObservation]:
    observations: list[FrontierObservation] = []
    for atom_id, node in graph.nodes.items():
        atom: KnowledgeAtom = node.atom
        degree = graph_degree(graph, atom_id)
        if degree == 0:
            observations.append(FrontierObservation(atom_id, FrontierType.ORPHAN_ATOM, 90, "Atom has no graph relations."))
        if not atom.evidence:
            observations.append(FrontierObservation(atom_id, FrontierType.LOW_EVIDENCE, 80, "Atom has no evidence entries."))
        if not atom.limitations:
            observations.append(FrontierObservation(atom_id, FrontierType.LOW_LIMITATION, 75, "Atom has no limitation entries."))
        if degree >= 5:
            observations.append(FrontierObservation(atom_id, FrontierType.HIGH_DEGREE, 60 + degree, "Atom is a possible hub or overloaded concept."))
        if degree == 1 and atom.evidence and atom.limitations:
            observations.append(FrontierObservation(atom_id, FrontierType.REVIEW_FOCUS, 65, "Atom is structured but weakly connected; good candidate for zoom review."))
    return sorted(observations, key=lambda item: item.score, reverse=True)


def write_frontiers(observations: list[FrontierObservation], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(obs) for obs in observations], indent=2, ensure_ascii=False), encoding="utf-8")
    return path
