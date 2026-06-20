from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReadinessSignal:
    name: str
    modules: int
    tests: int
    docs: int
    artifacts: int


@dataclass(frozen=True)
class ReadinessReport:
    score: float
    status: str
    markdown: str


class AITReadiness:
    def score(self, item: ReadinessSignal) -> float:
        value = min(item.modules, 12) * 0.45
        value += min(item.tests, 20) * 0.16
        value += min(item.docs, 20) * 0.12
        value += min(item.artifacts, 12) * 0.12
        return round(min(value, 10.0), 2)

    def status(self, score: float) -> str:
        if score >= 8.5:
            return "strong"
        if score >= 7.0:
            return "good"
        if score >= 5.0:
            return "growing"
        return "seed"

    def report(self, item: ReadinessSignal) -> ReadinessReport:
        score = self.score(item)
        status = self.status(score)
        markdown = "# AIT Readiness\n\n" + f"Name: `{item.name}`\nScore: `{score}`\nStatus: `{status}`\n"
        return ReadinessReport(score, status, markdown)
