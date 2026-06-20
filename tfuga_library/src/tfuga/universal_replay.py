from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev
from math import sqrt


@dataclass(frozen=True)
class ReplayTask:
    date: str
    name: str
    signal: float
    expected: str
    weight: float = 1.0


@dataclass(frozen=True)
class ReplayModel:
    name: str
    family: str
    threshold: float = 0.5
    limit: float = 0.5


@dataclass(frozen=True)
class ReplayOutcome:
    name: str
    average_score: float
    risk: float
    stability: float
    blocked: int
    total_score: float


class AITUniversalReplay:
    def decide(self, task: ReplayTask, model: ReplayModel) -> tuple[str, float]:
        x = task.signal
        if model.family == "cautious":
            if abs(x) < model.threshold:
                return "hold", abs(x) * 0.25
            return ("positive" if x > 0 else "negative", min(abs(x), 1.0))
        if model.family == "fast":
            if abs(x) < model.threshold * 0.5:
                return "hold", abs(x) * 0.4
            return ("positive" if x > 0 else "negative", min(abs(x) * 1.3, 1.0))
        if model.family == "validator":
            if task.weight < 0.75:
                return "hold", 0.1
            return ("positive" if x >= 0 else "negative", min(abs(x), 1.0))
        return "hold", 0.0

    def score_step(self, action: str, expected: str, risk: float, weight: float) -> float:
        if action == expected:
            base = 1.0
        elif action == "hold" and expected != "hold":
            base = 0.35
        elif expected == "hold" and action != "hold":
            base = -0.25
        else:
            base = -0.5
        return (base - risk * 0.25) * weight

    def run_one(self, tasks: tuple[ReplayTask, ...], model: ReplayModel) -> ReplayOutcome:
        if not tasks:
            raise ValueError("Need tasks.")
        scores = []
        risks = []
        blocked = 0
        for task in tasks:
            action, risk = self.decide(task, model)
            if risk > model.limit:
                action = "hold"
                blocked += 1
            scores.append(self.score_step(action, task.expected, risk, task.weight))
            risks.append(risk)
        avg = mean(scores)
        r = mean(risks)
        stability = 1.0 / (1.0 + (pstdev(scores) if len(scores) > 1 else 0.0) * sqrt(len(scores)))
        total = round(avg * 100.0 - r * 25.0 - blocked * 2.0 + stability * 10.0, 4)
        return ReplayOutcome(model.name, round(avg, 6), round(r, 6), round(stability, 6), blocked, total)

    def defaults(self) -> tuple[ReplayModel, ...]:
        return (
            ReplayModel("jkd", "cautious", threshold=0.45, limit=0.55),
            ReplayModel("yy3", "fast", threshold=0.45, limit=0.65),
            ReplayModel("oak", "validator", threshold=0.35, limit=0.4),
        )

    def demo_tasks(self) -> tuple[ReplayTask, ...]:
        return (
            ReplayTask("2024-01-01", "validate", 0.7, "positive", 1.0),
            ReplayTask("2024-01-02", "safety", -0.8, "hold", 1.2),
            ReplayTask("2024-01-03", "research", 0.2, "positive", 0.8),
            ReplayTask("2024-01-04", "low confidence", -0.15, "hold", 1.0),
        )

    def run_all(self, tasks: tuple[ReplayTask, ...]) -> tuple[ReplayOutcome, ...]:
        return tuple(self.run_one(tasks, model) for model in self.defaults())
