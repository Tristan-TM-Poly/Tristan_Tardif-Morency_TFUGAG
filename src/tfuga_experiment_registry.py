"""Experiment Registry for TFUGAG.

Links research questions and claims to minimal test plans. The registry stores
plans and results as reviewable records; it does not claim that a result is
scientific proof without external review.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

from src.tfuga_question_engine import ResearchQuestion


class ExperimentStatus(str, Enum):
    PROPOSED = "proposed"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    INCONCLUSIVE = "inconclusive"
    ARCHIVED = "archived"


@dataclass(frozen=True)
class ExperimentPlan:
    experiment_id: str
    question: str
    hypothesis: str
    method: str
    required_inputs: list[str]
    success_criteria: list[str]
    failure_criteria: list[str]
    status: ExperimentStatus = ExperimentStatus.PROPOSED


@dataclass(frozen=True)
class ExperimentResult:
    experiment_id: str
    status: ExperimentStatus
    observations: list[str]
    conclusion: str
    next_action: str


def plan_from_question(question: ResearchQuestion) -> ExperimentPlan:
    return ExperimentPlan(
        experiment_id=f"exp_{question.atom_id}",
        question=question.question,
        hypothesis="A minimal test can reduce uncertainty around this frontier.",
        method="Define a small reproducible check, calculation, simulation, or literature comparison.",
        required_inputs=["atom definition", "claim text", "assumptions", "candidate evidence"],
        success_criteria=["uncertainty reduced", "status recommendation produced", "limitations updated"],
        failure_criteria=["claim remains ambiguous", "missing data", "contradictory evidence"],
    )


def write_experiment_plan(plan: ExperimentPlan, output_dir: str | Path = "experiments/plans") -> Path:
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{plan.experiment_id}.json"
    path.write_text(json.dumps(asdict(plan), indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def write_experiment_result(result: ExperimentResult, output_dir: str | Path = "experiments/results") -> Path:
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{result.experiment_id}.json"
    path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=False), encoding="utf-8")
    return path
