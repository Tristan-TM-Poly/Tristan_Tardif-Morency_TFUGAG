"""Question Engine for TFUGAG.

Turns frontier observations into reviewable research questions. Questions are
not answers; they are prompts for evidence, experiments, definitions, or bridge
review.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from pathlib import Path

from src.tfuga_frontier_detector import FrontierObservation, FrontierType


@dataclass(frozen=True)
class ResearchQuestion:
    atom_id: str
    question: str
    reason: str
    priority: int


def question_from_frontier(obs: FrontierObservation) -> ResearchQuestion:
    templates = {
        FrontierType.ORPHAN_ATOM: "Which existing atoms should this atom connect to, and by which relation type?",
        FrontierType.LOW_EVIDENCE: "What is the smallest proof, calculation, simulation, or observation that could support this claim?",
        FrontierType.LOW_LIMITATION: "Where does this claim fail, and what boundary conditions should be declared?",
        FrontierType.HIGH_DEGREE: "Is this hub concept overloaded, or should it be split into smaller atoms?",
        FrontierType.REVIEW_FOCUS: "Which preventive subgraph should be generated around this focus next?",
    }
    return ResearchQuestion(
        atom_id=obs.atom_id,
        question=templates[obs.frontier_type],
        reason=obs.rationale,
        priority=obs.score,
    )


def questions_from_frontiers(observations: list[FrontierObservation]) -> list[ResearchQuestion]:
    return sorted([question_from_frontier(obs) for obs in observations], key=lambda q: q.priority, reverse=True)


def write_questions(questions: list[ResearchQuestion], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(question) for question in questions], indent=2, ensure_ascii=False), encoding="utf-8")
    return path
