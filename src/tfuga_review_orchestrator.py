"""TFUGAG Review Orchestrator.

This is a zero-mutation orchestrator: it connects existing TFUGAG engines into
one review pipeline, but it does not call external APIs, execute arbitrary model
output, push to main, or deploy anything. Its output is a review bundle.
"""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

from src.tfuga_airgap import KnowledgeAtom
from src.tfuga_atlas_builder import build_atlas
from src.tfuga_experiment_registry import plan_from_question
from src.tfuga_frontier_detector import detect_frontiers
from src.tfuga_graph import KnowledgeGraph
from src.tfuga_promotion_engine import evaluate_all
from src.tfuga_proposal_engine import proposals_from_atoms
from src.tfuga_question_engine import questions_from_frontiers


def build_review_bundle(graph: KnowledgeGraph, atoms: dict[str, KnowledgeAtom]) -> dict:
    frontiers = detect_frontiers(graph)
    questions = questions_from_frontiers(frontiers)
    experiments = [plan_from_question(question) for question in questions]
    promotions = evaluate_all(atoms)
    proposals = proposals_from_atoms(atoms)
    atlas = build_atlas(graph, frontiers)

    return {
        "schema": "tfugag.review_bundle.v1",
        "summary": {
            "atoms": len(atoms),
            "frontiers": len(frontiers),
            "questions": len(questions),
            "experiments": len(experiments),
            "promotion_packets": len(promotions),
            "system_proposals": len(proposals),
        },
        "atlas": atlas,
        "frontiers": [asdict(item) for item in frontiers],
        "questions": [asdict(item) for item in questions],
        "experiments": [asdict(item) for item in experiments],
        "promotions": [asdict(item) for item in promotions],
        "proposals": [item.to_dict() for item in proposals],
    }


def write_review_bundle(bundle: dict, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding="utf-8")
    return path
