"""TFUGAG Omega Graph.

Common data model for unifying TFUGAG layers. Everything becomes an OmegaNode:
atom, claim, source, evidence, question, protocol, result, bridge, governance
rule, valuation, or atlas focus. Relations become typed OmegaEdges.

This module is descriptive and structural only. It does not execute actions,
call external services, deploy systems, or mutate canon.
"""
from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

class OmegaNodeKind(str, Enum):
    ATOM = "atom"
    CLAIM = "claim"
    SOURCE = "source"
    EVIDENCE = "evidence"
    QUESTION = "question"
    PROTOCOL = "protocol"
    RESULT = "result"
    BRIDGE = "bridge"
    FRONTIER = "frontier"
    RISK = "risk"
    APPLICATION = "application"
    GOVERNANCE_RULE = "governance_rule"
    VALUATION = "valuation"
    ATLAS_FOCUS = "atlas_focus"

class OmegaEdgeKind(str, Enum):
    SUPPORTS = "supports"
    REFUTES = "refutes"
    QUALIFIES = "qualifies"
    DEPENDS_ON = "depends_on"
    EXTENDS = "extends"
    ANALOGOUS_TO = "analogous_to"
    CONTRADICTS = "contradicts"
    GENERATES = "generates"
    CONTAINS = "contains"
    PRIORITIZES = "prioritizes"
    REVIEWS = "reviews"
    PROMOTES = "promotes"
    ARCHIVES = "archives"
    VALUES = "values"

@dataclass(frozen=True)
class OmegaState:
    status: str
    confidence: float = 0.0
    oak_flags: list[str] | None = None

@dataclass(frozen=True)
class OmegaNode:
    node_id: str
    kind: OmegaNodeKind
    title: str
    content: str
    state: OmegaState
    metadata: dict

@dataclass(frozen=True)
class OmegaEdge:
    source_id: str
    target_id: str
    kind: OmegaEdgeKind
    rationale: str
    weight: float = 1.0
    evidence_refs: list[str] | None = None

@dataclass
class OmegaGraph:
    nodes: dict
    edges: list

    @classmethod
    def empty(cls):
        return cls({}, [])

    def add_node(self, node: OmegaNode):
        self.nodes[node.node_id] = node

    def add_edge(self, edge: OmegaEdge):
        self.edges.append(edge)

    def neighbors(self, node_id: str) -> list[str]:
        return [edge.target_id for edge in self.edges if edge.source_id == node_id]

    def to_dict(self):
        return {
            "schema": "tfugag.omega_graph.v1",
            "nodes": [asdict(node) for node in self.nodes.values()],
            "edges": [asdict(edge) for edge in self.edges],
        }


def write_omega_graph(graph: OmegaGraph, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(graph.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    return path
