from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VentureBlueprint:
    name: str
    kind: str
    purpose: str
    roles: tuple[str, ...]


@dataclass(frozen=True)
class VenturePlan:
    venture: VentureBlueprint
    score: float
    steps: tuple[str, ...]
    note: str


class AITVentureSetup:
    def defaults(self) -> tuple[VentureBlueprint, ...]:
        return (
            VentureBlueprint("TFUGA Labs", "operating", "software prototypes and services", ("software", "research", "services")),
            VentureBlueprint("OAK Systems", "asset", "verification assets and licenses", ("assets", "licensing", "verification")),
            VentureBlueprint("AIT Ventures", "portfolio", "ventures and partnerships", ("portfolio", "funding", "partnerships")),
            VentureBlueprint("HGFM Research", "research", "open research and education", ("research", "education", "publishing")),
        )

    def score(self, venture: VentureBlueprint) -> float:
        value = 2.0 + (1.0 if venture.name else 0.0) + (1.0 if venture.purpose else 0.0)
        value += min(len(venture.roles), 4) * 0.5
        return round(min(value, 10.0), 2)

    def plan(self, venture: VentureBlueprint) -> VenturePlan:
        return VenturePlan(
            venture,
            self.score(venture),
            ("name review", "route choice", "owner data", "structure", "accounts", "handoff"),
            "Prepare packet; owner or representative completes official steps.",
        )

    def portfolio(self) -> tuple[VenturePlan, ...]:
        return tuple(self.plan(item) for item in self.defaults())

    def markdown(self) -> str:
        lines = ["# AIT Venture Setup", ""]
        for plan in self.portfolio():
            v = plan.venture
            lines.append(f"## {v.name}")
            lines.append(f"- kind: `{v.kind}`")
            lines.append(f"- score: `{plan.score}`")
            lines.append(f"- purpose: {v.purpose}")
            lines.append(f"- note: {plan.note}")
            lines.append("")
        return "\n".join(lines).strip() + "\n"
