from __future__ import annotations

from dataclasses import dataclass
from statistics import mean


@dataclass(frozen=True)
class ModelAnswer:
    model_id: str
    answer: str
    confidence: float
    cost_hint: float = 1.0
    latency_hint: float = 1.0


@dataclass(frozen=True)
class CouncilDecision:
    winner: ModelAnswer
    scores: dict[str, float]
    consensus: str
    oak_score: float


class LocalAICouncilAdapter:
    """Local-first council pattern for comparing model answers.

    This adapter scores already-produced answers. It does not perform inference
    or require external services.
    """

    def decide(self, answers: list[ModelAnswer]) -> CouncilDecision:
        if not answers:
            raise ValueError("at least one answer is required")
        scores: dict[str, float] = {}
        for item in answers:
            length_bonus = min(len(item.answer.strip()) / 500.0, 1.0)
            efficiency = 1.0 / max(item.cost_hint + item.latency_hint, 0.1)
            score = (item.confidence * 6.0) + (length_bonus * 2.0) + (efficiency * 2.0)
            scores[item.model_id] = round(max(0.0, min(10.0, score)), 3)
        winner = max(answers, key=lambda item: scores[item.model_id])
        avg = mean(scores.values())
        consensus = "high" if avg >= 7.0 else "medium" if avg >= 5.0 else "low"
        return CouncilDecision(winner=winner, scores=scores, consensus=consensus, oak_score=round(avg, 3))
