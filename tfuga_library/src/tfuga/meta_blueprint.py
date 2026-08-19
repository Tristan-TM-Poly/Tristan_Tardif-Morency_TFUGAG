from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MetaNeed:
    source: str
    capability: str
    evidence: str
    severity: float = 1.0


@dataclass(frozen=True)
class MetaBlueprint:
    name: str
    purpose: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    tests: tuple[str, ...]
    gates: tuple[str, ...]


@dataclass(frozen=True)
class MetaReadiness:
    score: float
    approved: bool
    notes: tuple[str, ...]


class AITMetaBlueprint:
    def name_for(self, need: MetaNeed) -> str:
        clean = "".join(ch if ch.isalnum() else "_" for ch in need.capability).strip("_")
        return f"AIT_{clean}_Factory"

    def build(self, need: MetaNeed) -> MetaBlueprint:
        return MetaBlueprint(
            self.name_for(need),
            f"Prepare a factory plan for: {need.capability}",
            ("artifact", "schema", "examples", "review gates"),
            ("module", "tests", "docs", "manifest"),
            ("reject empty input", "parse minimal sample", "deterministic output"),
            ("static review", "dry run", "tests", "human review"),
        )

    def readiness(self, blueprint: MetaBlueprint) -> MetaReadiness:
        score = 0.0
        notes = []
        if blueprint.inputs:
            score += 2.0
            notes.append("inputs")
        if blueprint.outputs:
            score += 2.0
            notes.append("outputs")
        if len(blueprint.tests) >= 3:
            score += 3.0
            notes.append("tests")
        if len(blueprint.gates) >= 4:
            score += 3.0
            notes.append("gates")
        return MetaReadiness(round(score, 2), score >= 9.0, tuple(notes))

    def propose(self, needs: tuple[MetaNeed, ...]) -> tuple[tuple[MetaBlueprint, MetaReadiness], ...]:
        pairs = []
        for need in needs:
            if need.severity > 0:
                blueprint = self.build(need)
                pairs.append((blueprint, self.readiness(blueprint)))
        return tuple(pairs)
