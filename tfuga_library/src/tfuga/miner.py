from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class ProblemSeed:
    id: str
    domain: str
    target: str
    graph_form: str
    expected_output: str


class GraphProblemMiner:
    def __init__(self, seeds: Iterable[ProblemSeed]) -> None:
        self.seeds = list(seeds)

    def rank(self, seed: ProblemSeed) -> float:
        text = " ".join([seed.domain, seed.target, seed.graph_form, seed.expected_output]).lower()
        score = 0.0
        if "graph" in text or "graphe" in text or "hyper" in text:
            score += 3.0
        if "certificate" in text or "certificat" in text or "sat" in text or "classification" in text:
            score += 2.5
        if "small" in text or "petit" in text or "finite" in text or "fini" in text:
            score += 2.0
        if "bound" in text or "borne" in text or "counterexample" in text or "contre-exemple" in text:
            score += 1.5
        return min(score, 10.0)

    def top(self, n: int = 10) -> list[tuple[ProblemSeed, float]]:
        ranked = [(seed, self.rank(seed)) for seed in self.seeds]
        return sorted(ranked, key=lambda item: item[1], reverse=True)[:n]
