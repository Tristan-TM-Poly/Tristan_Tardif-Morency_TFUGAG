"""TFUGAG Omega Atlas Engine.

Builds navigable atlas views from OmegaGraph-derived structures.
The atlas is a projection layer that organizes structure, evidence,
contradictions, frontiers, evolution, applications, and valuation.
"""
from dataclasses import dataclass, asdict
import json
from pathlib import Path

@dataclass(frozen=True)
class AtlasView:
    focus_node_id: str
    structure_refs: list[str]
    evidence_refs: list[str]
    contradiction_refs: list[str]
    frontier_refs: list[str]
    evolution_refs: list[str]
    application_refs: list[str]
    valuation_refs: list[str]


def build_atlas_view(focus_node_id: str) -> AtlasView:
    return AtlasView(
        focus_node_id=focus_node_id,
        structure_refs=[],
        evidence_refs=[],
        contradiction_refs=[],
        frontier_refs=[],
        evolution_refs=[],
        application_refs=[],
        valuation_refs=[],
    )


def write_atlas_view(view: AtlasView, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(view), indent=2, ensure_ascii=False), encoding='utf-8')
    return path
