"""TFUGAG Evidence Graph.

Separates claims, evidence, sources, and experiments as first-class graph
objects. This makes support, refutation, and uncertainty traceable instead of
burying them inside atom text.
"""
from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

class EvidenceRelation(str, Enum):
    SUPPORTS = "supports"
    REFUTES = "refutes"
    QUALIFIES = "qualifies"
    DEPENDS_ON = "depends_on"

@dataclass(frozen=True)
class ClaimNode:
    claim_id: str
    text: str
    atom_id: str

@dataclass(frozen=True)
class EvidenceNode:
    evidence_id: str
    summary: str
    source_id: str
    confidence: float

@dataclass(frozen=True)
class SourceNode:
    source_id: str
    title: str
    locator: str
    source_type: str

@dataclass(frozen=True)
class EvidenceEdge:
    claim_id: str
    evidence_id: str
    relation: EvidenceRelation
    rationale: str

@dataclass
class EvidenceGraph:
    claims: dict
    evidence: dict
    sources: dict
    edges: list

    @classmethod
    def empty(cls):
        return cls({}, {}, {}, [])

    def add_claim(self, node: ClaimNode):
        self.claims[node.claim_id] = node

    def add_evidence(self, node: EvidenceNode):
        self.evidence[node.evidence_id] = node

    def add_source(self, node: SourceNode):
        self.sources[node.source_id] = node

    def link(self, edge: EvidenceEdge):
        self.edges.append(edge)

    def to_dict(self):
        return {
            "schema": "tfugag.evidence_graph.v1",
            "claims": [asdict(v) for v in self.claims.values()],
            "evidence": [asdict(v) for v in self.evidence.values()],
            "sources": [asdict(v) for v in self.sources.values()],
            "edges": [asdict(e) for e in self.edges],
        }


def write_evidence_graph(graph: EvidenceGraph, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(graph.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    return path
