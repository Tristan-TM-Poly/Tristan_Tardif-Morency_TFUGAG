"""Minimal TFUGAG knowledge graph utilities.

The graph is intentionally small and deterministic. It models reviewed
Knowledge Atoms as nodes and typed relations as edges.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

from src.tfuga_airgap import KnowledgeAtom


class RelationType(str, Enum):
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    GENERALIZES = "generalizes"
    SPECIALIZES = "specializes"
    ANALOGOUS_TO = "analogous_to"
    DEPENDS_ON = "depends_on"


@dataclass(frozen=True)
class AtomNode:
    atom_id: str
    atom: KnowledgeAtom


@dataclass(frozen=True)
class AtomRelation:
    source_id: str
    target_id: str
    relation: RelationType
    rationale: str


class KnowledgeGraph:
    def __init__(self) -> None:
        self.nodes: dict[str, AtomNode] = {}
        self.edges: list[AtomRelation] = []

    def add_atom(self, atom_id: str, atom: KnowledgeAtom) -> None:
        if not atom_id.strip():
            raise ValueError("atom_id must not be empty")
        if atom_id in self.nodes:
            raise ValueError(f"duplicate atom_id: {atom_id}")
        self.nodes[atom_id] = AtomNode(atom_id=atom_id, atom=atom)

    def add_relation(self, source_id: str, target_id: str, relation: RelationType, rationale: str) -> None:
        if source_id not in self.nodes:
            raise KeyError(f"unknown source atom: {source_id}")
        if target_id not in self.nodes:
            raise KeyError(f"unknown target atom: {target_id}")
        if source_id == target_id:
            raise ValueError("self-relations are not allowed in the minimal graph")
        if not rationale.strip():
            raise ValueError("rationale must not be empty")
        self.edges.append(
            AtomRelation(
                source_id=source_id,
                target_id=target_id,
                relation=relation,
                rationale=rationale,
            )
        )

    def neighbors(self, atom_id: str) -> list[AtomRelation]:
        return [edge for edge in self.edges if edge.source_id == atom_id or edge.target_id == atom_id]

    def to_dict(self) -> dict:
        return {
            "nodes": [
                {
                    "atom_id": node.atom_id,
                    "atom": asdict(node.atom),
                }
                for node in self.nodes.values()
            ],
            "edges": [asdict(edge) for edge in self.edges],
        }

    def write_json(self, output_path: str | Path) -> Path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
        return path
