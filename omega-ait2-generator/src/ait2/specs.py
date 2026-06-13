from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass(frozen=True)
class AITSpec:
    """A minimal genome for an AIT.

    The spec keeps generated agents explicit: mission, inputs, outputs,
    validators, memory, yield targets, and an OAK maturity threshold.
    """

    name: str
    mission: str
    inputs: list[str]
    outputs: list[str]
    tools: list[str]
    validators: list[str]
    memory_read: list[str]
    memory_write: list[str]
    yield_targets: list[str]
    oak_min_status: int = 2
    assumptions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class OAKReport:
    """Operational Analysis Kernel report.

    OAK separates validated structure from weaknesses and residues. A high
    score is not a proof; it is a promotion signal that must remain auditable.
    """

    status: int
    strengths: list[str]
    weaknesses: list[str]
    residues: list[str]
    tests: list[str]
    next_actions: list[str]

    @property
    def is_promotable(self) -> bool:
        return self.status >= 2 and len(self.tests) > 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AITPacket:
    """Generated AIT artifact with traceable intermediate products."""

    spec: AITSpec
    hgfm: dict[str, Any]
    cvcd_score: float
    oak_report: OAKReport
    residues: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec": self.spec.to_dict(),
            "hgfm": self.hgfm,
            "cvcd_score": self.cvcd_score,
            "oak_report": self.oak_report.to_dict(),
            "residues": self.residues,
        }
