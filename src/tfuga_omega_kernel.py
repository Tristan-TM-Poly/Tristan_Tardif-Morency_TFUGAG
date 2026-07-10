"""TFUGAG Omega Kernel.

Analytical kernel for OmegaGraph. It computes structural densities and frontier
signals from the unified graph model. This module is read-only: it does not
execute actions, call APIs, deploy, or mutate canon.
"""
from dataclasses import dataclass, asdict
import json
from pathlib import Path

from src.tfuga_omega_graph import OmegaGraph, OmegaNodeKind, OmegaEdgeKind

@dataclass(frozen=True)
class OmegaRegionSignal:
    node_id: str
    degree: int
    evidence_density: float
    contradiction_density: float
    bridge_density: float
    question_density: float
    frontier_score: float
    recommendation: str


def _out_edges(graph: OmegaGraph, node_id: str):
    return [edge for edge in graph.edges if edge.source_id == node_id]


def _count_edges(edges, kind: OmegaEdgeKind) -> int:
    return sum(1 for edge in edges if edge.kind == kind)


def analyze_node(graph: OmegaGraph, node_id: str) -> OmegaRegionSignal:
    edges = _out_edges(graph, node_id)
    degree = len(edges)
    denom = max(1, degree)

    evidence = _count_edges(edges, OmegaEdgeKind.SUPPORTS) + _count_edges(edges, OmegaEdgeKind.QUALIFIES)
    contradictions = _count_edges(edges, OmegaEdgeKind.REFUTES) + _count_edges(edges, OmegaEdgeKind.CONTRADICTS)
    bridges = _count_edges(edges, OmegaEdgeKind.ANALOGOUS_TO) + _count_edges(edges, OmegaEdgeKind.EXTENDS)
    questions = _count_edges(edges, OmegaEdgeKind.GENERATES)

    evidence_density = evidence / denom
    contradiction_density = contradictions / denom
    bridge_density = bridges / denom
    question_density = questions / denom

    frontier_score = (1.0 - evidence_density) + contradiction_density + (1.0 - bridge_density) + question_density

    if contradiction_density > 0.25:
        recommendation = "quarantine_review"
    elif evidence_density < 0.25:
        recommendation = "seek_evidence"
    elif bridge_density < 0.25:
        recommendation = "seek_bridges"
    elif question_density > 0.5:
        recommendation = "plan_research"
    else:
        recommendation = "monitor"

    return OmegaRegionSignal(
        node_id=node_id,
        degree=degree,
        evidence_density=evidence_density,
        contradiction_density=contradiction_density,
        bridge_density=bridge_density,
        question_density=question_density,
        frontier_score=frontier_score,
        recommendation=recommendation,
    )


def analyze_graph(graph: OmegaGraph) -> list[OmegaRegionSignal]:
    signals = [analyze_node(graph, node_id) for node_id in graph.nodes.keys()]
    return sorted(signals, key=lambda signal: signal.frontier_score, reverse=True)


def write_omega_signals(signals: list[OmegaRegionSignal], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(signal) for signal in signals], indent=2, ensure_ascii=False), encoding="utf-8")
    return path
