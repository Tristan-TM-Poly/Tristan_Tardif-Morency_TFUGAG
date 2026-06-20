from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BuildNeed:
    source: str
    capability: str
    evidence: str
    priority: float = 1.0


@dataclass(frozen=True)
class BuildPlan:
    name: str
    files: tuple[str, ...]
    tests: tuple[str, ...]
    gates: tuple[str, ...]
    score: float
    approved: bool = False


class AITBuildQueue:
    gates = ("static review", "dry run", "tests", "docs", "approval")

    def name_for(self, capability: str) -> str:
        clean = "".join(ch if ch.isalnum() else "_" for ch in capability).strip("_")
        return f"AIT_{clean}_Builder"

    def plan(self, need: BuildNeed) -> BuildPlan:
        name = self.name_for(need.capability)
        stem = name.lower()
        files = (f"src/tfuga/{stem}.py",)
        tests = (f"tests/test_{stem}.py",)
        score = 10.0 if need.priority > 0 else 0.0
        return BuildPlan(name, files, tests, self.gates, score, False)

    def queue(self, needs: tuple[BuildNeed, ...]) -> tuple[BuildPlan, ...]:
        return tuple(self.plan(need) for need in needs if need.priority > 0)

    def demo_needs(self) -> tuple[BuildNeed, ...]:
        return (
            BuildNeed("void", "parquet absorber", "unsupported file", 1.0),
            BuildNeed("status", "cad absorber", "missing parser", 0.9),
            BuildNeed("replay", "multi asset replay", "single series", 0.8),
        )

    def markdown(self, plans: tuple[BuildPlan, ...]) -> str:
        lines = ["# AIT Build Queue", "", "mode: dry_run", ""]
        for plan in plans:
            lines.append(f"## {plan.name}")
            lines.append(f"- score: `{plan.score}`")
            lines.append(f"- approved: `{plan.approved}`")
            lines.append(f"- gates: `{', '.join(plan.gates)}`")
            lines.append("")
        return "\n".join(lines).strip() + "\n"
