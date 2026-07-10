from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IPDisclosure:
    title: str
    field: str
    problem: str
    solution: str
    inventors: tuple[str, ...]
    markets: tuple[str, ...] = ("Canada",)


@dataclass(frozen=True)
class IPDocketPlan:
    route: str
    readiness: float
    sections: tuple[str, ...]
    gates: tuple[str, ...]
    handoff: str


class AITIPDocket:
    sections = (
        "title",
        "field",
        "background",
        "summary",
        "detailed description",
        "embodiments",
        "claims skeleton",
        "abstract",
        "inventor data",
        "prior art list",
        "disclosure log",
    )

    def score(self, item: IPDisclosure) -> float:
        value = 0.0
        for text in (item.title, item.field, item.problem, item.solution):
            if text.strip():
                value += 1.5
        value += min(len(item.inventors), 3) * 0.5
        value += min(len(item.markets), 4) * 0.4
        return round(min(value, 10.0), 2)

    def plan(self, item: IPDisclosure, route: str = "CIPO") -> IPDocketPlan:
        gates = (
            "confidentiality review",
            "prior art search",
            "inventor review",
            "claim review",
            "official portal handoff",
        )
        if route.upper() == "PCT":
            handoff = "Prepare ePCT handoff packet; applicant or representative submits and pays official fees."
        elif route.upper() == "USPTO":
            handoff = "Prepare Patent Center packet; applicant or practitioner submits and signs."
        else:
            handoff = "Prepare CIPO/MyCIPO packet; applicant or patent agent submits and pays official fees."
        return IPDocketPlan(route, self.score(item), self.sections, gates, handoff)

    def markdown(self, item: IPDisclosure, route: str = "CIPO") -> str:
        plan = self.plan(item, route)
        lines = ["# AIT IP Docket", "", f"Title: `{item.title}`", f"Route: `{plan.route}`", f"Readiness: `{plan.readiness}`", "", "## Sections"]
        lines += [f"- [ ] {section}" for section in plan.sections]
        lines += ["", "## Gates"]
        lines += [f"- [ ] {gate}" for gate in plan.gates]
        lines += ["", "## Official handoff", "", plan.handoff]
        return "\n".join(lines).strip() + "\n"
