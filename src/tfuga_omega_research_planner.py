"""TFUGAG Omega Research Planner.

Transforms OmegaQuestion objects into prioritized research candidates.
This module is planning-only: it does not execute protocols, call models,
access the web, deploy, or mutate canon.
"""
from dataclasses import dataclass, asdict
import json
from pathlib import Path

from src.tfuga_omega_question_engine import OmegaQuestion

@dataclass(frozen=True)
class OmegaResearchCandidate:
    candidate_id: str
    source_question_id: str
    node_id: str
    objective: str
    dependencies: list[str]
    expected_deliverables: list[str]
    validation_route: str
    priority: float


def candidate_from_question(question: OmegaQuestion) -> OmegaResearchCandidate:
    if question.question_type == "evidence_gap":
        deps = ["source review", "evidence object", "claim mapping"]
        deliverables = ["evidence node", "support or refute edge", "confidence update"]
        route = "Evidence Graph -> OmegaPromotion"
    elif question.question_type == "bridge_gap":
        deps = ["candidate neighbor domain", "relation rationale"]
        deliverables = ["bridge node", "analogous_to or depends_on edge", "bridge review packet"]
        route = "Bridge Engine -> OmegaKernel"
    elif question.question_type == "contradiction_resolution":
        deps = ["conflict pair", "assumptions", "evidence refs"]
        deliverables = ["quarantine packet", "resolution proposal", "evolution event"]
        route = "OAK Quarantine -> OmegaEvolution"
    elif question.question_type == "protocol_candidate":
        deps = ["research objective", "expected output", "safety constraints"]
        deliverables = ["protocol record", "result placeholder", "evidence mapping"]
        route = "Protocol Registry -> Evidence Graph"
    else:
        deps = ["focus node", "atlas lens"]
        deliverables = ["atlas view", "frontier refs", "question refs"]
        route = "OmegaAtlas -> OmegaFrontier"

    return OmegaResearchCandidate(
        candidate_id=f"rc_{question.question_id}",
        source_question_id=question.question_id,
        node_id=question.node_id,
        objective=question.question,
        dependencies=deps,
        expected_deliverables=deliverables,
        validation_route=route,
        priority=question.priority,
    )


def candidates_from_questions(questions: list[OmegaQuestion]) -> list[OmegaResearchCandidate]:
    return sorted([candidate_from_question(question) for question in questions], key=lambda c: c.priority, reverse=True)


def write_omega_research_candidates(candidates: list[OmegaResearchCandidate], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(candidate) for candidate in candidates], indent=2, ensure_ascii=False), encoding="utf-8")
    return path
