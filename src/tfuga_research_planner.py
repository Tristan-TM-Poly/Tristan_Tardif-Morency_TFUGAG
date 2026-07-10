"""TFUGAG Research Planner Engine.

Prioritizes research actions from frontiers, questions, and experiments.
It produces a roadmap; it does not execute experiments or mutate canon.
"""
from dataclasses import dataclass, asdict
import json
from pathlib import Path

@dataclass(frozen=True)
class ResearchTask:
    task_id: str
    title: str
    information_gain: int
    cost: int
    urgency: int
    oak_risk: int
    next_action: str

@dataclass(frozen=True)
class RoadmapItem:
    task: ResearchTask
    priority_score: float
    rank: int


def score_task(task: ResearchTask) -> float:
    return (task.information_gain * 2 + task.urgency) - (task.cost + task.oak_risk)


def build_roadmap(tasks: list[ResearchTask]) -> list[RoadmapItem]:
    ordered = sorted(tasks, key=score_task, reverse=True)
    return [RoadmapItem(task=t, priority_score=score_task(t), rank=i + 1) for i, t in enumerate(ordered)]


def write_roadmap(items: list[RoadmapItem], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(item) for item in items], indent=2, ensure_ascii=False), encoding="utf-8")
    return path
