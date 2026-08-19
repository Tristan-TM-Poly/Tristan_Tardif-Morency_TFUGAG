"""TFUGAG Omega Frontier Engine.

Transforms OmegaKernel signals into candidate research frontiers. It generates
questions and priorities as reviewable outputs only. It does not call models,
run experiments, access the web, deploy, or mutate canon.
"""
from dataclasses import dataclass, asdict
import json
from pathlib import Path

from src.tfuga_omega_kernel import OmegaRegionSignal

@dataclass(frozen=True)
class OmegaFrontier:
    frontier_id: str
    node_id: str
    priority: float
    question: str
    reason: str
    recommended_route: str


def frontier_from_signal(signal: OmegaRegionSignal) -> OmegaFrontier:
    if signal.recommendation == "quarantine_review":
        question = "Which claim, evidence, or bridge creates the contradiction pressure around this node?"
        route = "OAK quarantine review"
    elif signal.recommendation == "seek_evidence":
        question = "What is the smallest evidence object that could support, qualify, or refute this node?"
        route = "Evidence Graph"
    elif signal.recommendation == "seek_bridges":
        question = "Which adjacent domain or atom should be bridged to reduce isolation around this node?"
        route = "Bridge Engine"
    elif signal.recommendation == "plan_research":
        question = "Which generated question should become the next research protocol candidate?"
        route = "Research Planner"
    else:
        question = "Should this node remain monitored or be expanded through the fractal atlas?"
        route = "Fractal Atlas"

    return OmegaFrontier(
        frontier_id=f"frontier_{signal.node_id}",
        node_id=signal.node_id,
        priority=signal.frontier_score,
        question=question,
        reason=f"Recommendation={signal.recommendation}; evidence={signal.evidence_density:.2f}; contradictions={signal.contradiction_density:.2f}; bridges={signal.bridge_density:.2f}; questions={signal.question_density:.2f}",
        recommended_route=route,
    )


def frontiers_from_signals(signals: list[OmegaRegionSignal]) -> list[OmegaFrontier]:
    return sorted([frontier_from_signal(signal) for signal in signals], key=lambda item: item.priority, reverse=True)


def write_omega_frontiers(frontiers: list[OmegaFrontier], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(frontier) for frontier in frontiers], indent=2, ensure_ascii=False), encoding="utf-8")
    return path
