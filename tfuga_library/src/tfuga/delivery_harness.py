from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DeliverySignal:
    changed_files: int
    additions: int
    tests_added: int
    docs_added: int
    review_notes: int = 0
    ci_failures: int = 0


@dataclass(frozen=True)
class DeliveryAssessment:
    risk: str
    oak_score: float
    hidden_work_index: float
    required_gates: tuple[str, ...]


class DeliveryHarnessAdapter:
    """Quality gate for AI-speed delivery."""

    def assess(self, signal: DeliverySignal) -> DeliveryAssessment:
        size_pressure = min((signal.changed_files / 20.0) + (signal.additions / 1000.0), 4.0)
        quality_credit = min(signal.tests_added * 0.7 + signal.docs_added * 0.4, 3.0)
        friction = min(signal.review_notes * 0.3 + signal.ci_failures * 1.2, 3.0)
        hidden_work = round(max(0.0, size_pressure + friction - quality_credit), 3)
        oak_score = round(max(0.0, min(10.0, 8.0 - hidden_work + quality_credit)), 3)
        risk = "low" if hidden_work < 1.5 else "medium" if hidden_work < 3.0 else "high"
        gates = ["tests", "docs", "review"]
        if signal.ci_failures:
            gates.append("ci_remediation")
        if hidden_work >= 2.5:
            gates.append("split_or_stage")
        return DeliveryAssessment(risk=risk, oak_score=oak_score, hidden_work_index=hidden_work, required_gates=tuple(gates))
