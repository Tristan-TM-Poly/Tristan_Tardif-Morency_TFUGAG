"""Atlas Builder for TFUGAG.

Builds a navigable JSON atlas from the current KnowledgeGraph plus optional
frontier observations. It does not edit the graph or canon.
"""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

from src.tfuga_frontier_detector import FrontierObservation
from src.tfuga_graph import KnowledgeGraph


def build_atlas(graph: KnowledgeGraph, frontiers: list[FrontierObservation] | None = None) -> dict:
    frontier_map: dict[str, list[dict]] = {}
    for obs in frontiers or []:
        frontier_map.setdefault(obs.atom_id, []).append(asdict(obs))

    nodes = []
    for atom_id, node in graph.nodes.items():
        atom = node.atom
        nodes.append(
            {
                "id": atom_id,
                "title": atom.title,
                "claim": atom.claim,
                "status": atom.status.value,
                "degree": len(graph.neighbors(atom_id)),
                "frontiers": frontier_map.get(atom_id, []),
            }
        )

    edges = [asdict(edge) for edge in graph.edges]
    return {
        "schema": "tfugag.atlas.v1",
        "summary": {
            "nodes": len(nodes),
            "edges": len(edges),
            "frontier_observations": sum(len(v) for v in frontier_map.values()),
        },
        "nodes": nodes,
        "edges": edges,
    }


def write_atlas(atlas: dict, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(atlas, indent=2, ensure_ascii=False), encoding="utf-8")
    return path
