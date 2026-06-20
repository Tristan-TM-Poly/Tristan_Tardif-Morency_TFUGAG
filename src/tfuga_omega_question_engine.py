"""TFUGAG Omega Question Engine.

Generates reviewable research questions from OmegaFrontier objects and OmegaNode
context. It does not call external models, access the web, execute experiments,
or mutate canon.
"""
from dataclasses import dataclass, asdict
import json
from pathlib import Path

from src.tfuga_omega_frontier_engine import OmegaFrontier

@dataclass(frozen=True)
class OmegaQuestion:
    question_id: str
    source_frontier_id: str
    node_id: str
    question: str
    question_type: str
    priority: float
    expected_output_kind: str


def question_from_frontier(frontier: OmegaFrontier) -> OmegaQuestion:
    route = frontier.recommended_route.lower()
    if "evidence" in route:
        qtype = "evidence_gap"
        expected = "evidence"
    elif "bridge" in route:
        qtype = "bridge_gap"
        expected = "bridge"
    elif "quarantine" in route:
        qtype = "contradiction_resolution"
        expected = "review_packet"
    elif "research" in route:
        qtype = "protocol_candidate"
        expected = "protocol"
    else:
        qtype = "atlas_expansion"
        expected = "atlas_view"

    return OmegaQuestion(
        question_id=f"q_{frontier.frontier_id}",
        source_frontier_id=frontier.frontier_id,
        node_id=frontier.node_id,
        question=frontier.question,
        question_type=qtype,
        priority=frontier.priority,
        expected_output_kind=expected,
    )


def questions_from_frontiers(frontiers: list[OmegaFrontier]) -> list[OmegaQuestion]:
    return sorted([question_from_frontier(frontier) for frontier in frontiers], key=lambda q: q.priority, reverse=True)


def write_omega_questions(questions: list[OmegaQuestion], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(question) for question in questions], indent=2, ensure_ascii=False), encoding="utf-8")
    return path
