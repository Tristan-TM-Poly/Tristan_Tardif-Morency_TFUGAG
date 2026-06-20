"""TFUGAG Omega Hypergraph Layer.

Represents multi-node relations as reviewable hyperedges. This layer supports
complex coupled relations across claims, evidence, protocols, applications,
risks, systems and theories.

It is structural only: no external calls, no autonomous execution, no canon
mutation.
"""
from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

class HyperedgeKind(str, Enum):
    COUPLED_CLAIM = "coupled_claim"
    THEORY_APPLICATION = "theory_application"
    EVIDENCE_CONTEXT = "evidence_context"
    PROTOCOL_CONTEXT = "protocol_context"
    CONTRADICTION_CLUSTER = "contradiction_cluster"
    MYCELIAL_NEIGHBORHOOD = "mycelial_neighborhood"

@dataclass(frozen=True)
class OmegaHyperedge:
    hyperedge_id: str
    kind: HyperedgeKind
    node_refs: list[str]
    relation_label: str
    rationale: str
    evidence_refs: list[str]
    risk_flags: list[str]

@dataclass(frozen=True)
class OmegaHypergraphView:
    view_id: str
    focus_node_ref: str
    hyperedge_refs: list[str]
    neighborhood_node_refs: list[str]
    next_zoom_refs: list[str]


def build_hyperedge(
    hyperedge_id: str,
    kind: HyperedgeKind,
    node_refs: list[str],
    relation_label: str,
    rationale: str,
    evidence_refs: list[str] | None = None,
    risk_flags: list[str] | None = None,
) -> OmegaHyperedge:
    return OmegaHyperedge(
        hyperedge_id=hyperedge_id,
        kind=kind,
        node_refs=node_refs,
        relation_label=relation_label,
        rationale=rationale,
        evidence_refs=evidence_refs or [],
        risk_flags=risk_flags or [],
    )


def build_hypergraph_view(focus_node_ref: str, hyperedges: list[OmegaHyperedge]) -> OmegaHypergraphView:
    neighborhood = []
    next_zoom = []
    for edge in hyperedges:
        for node_ref in edge.node_refs:
            if node_ref not in neighborhood:
                neighborhood.append(node_ref)
        if edge.kind in {HyperedgeKind.CONTRADICTION_CLUSTER, HyperedgeKind.MYCELIAL_NEIGHBORHOOD}:
            next_zoom.extend(edge.node_refs)
    return OmegaHypergraphView(
        view_id=f"hypergraph_view_{focus_node_ref}",
        focus_node_ref=focus_node_ref,
        hyperedge_refs=[edge.hyperedge_id for edge in hyperedges],
        neighborhood_node_refs=neighborhood,
        next_zoom_refs=sorted(set(next_zoom)),
    )


def write_hyperedges(hyperedges: list[OmegaHyperedge], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(edge) for edge in hyperedges], indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def write_hypergraph_view(view: OmegaHypergraphView, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(view), indent=2, ensure_ascii=False), encoding="utf-8")
    return path
