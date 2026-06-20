from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReleaseItem:
    name: str
    channel: str
    title: str
    body: str
    status: str
    gates: tuple[str, ...]


class AITReleaseQueue:
    gates = ("identity", "basis", "contact", "optout", "review")

    def items(self) -> tuple[ReleaseItem, ...]:
        return (
            ReleaseItem("research", "note", "TFUGA research update", "Research to verified artifacts.", "blocked", self.gates),
            ReleaseItem("technical", "note", "OAK technical update", "Readiness and verification workflow.", "blocked", self.gates),
            ReleaseItem("pilot", "note", "AIT pilot update", "Validation partners and pilot scope.", "blocked", self.gates),
            ReleaseItem("public", "post", "HGFM public update", "Graph, fractal and tensor research note.", "blocked", ("review", "accuracy")),
        )

    def calendar(self) -> tuple[str, ...]:
        return ("day 1 identity", "day 2 public note", "day 3 partner review", "day 5 pilot", "day 7 technical")

    def markdown(self) -> str:
        lines = ["# AIT Release Queue", "", "mode: draft_only", ""]
        for item in self.items():
            lines.append(f"## {item.name}")
            lines.append(f"- channel: `{item.channel}`")
            lines.append(f"- title: `{item.title}`")
            lines.append(f"- status: `{item.status}`")
            lines.append(f"- gates: `{', '.join(item.gates)}`")
            lines.append(item.body)
            lines.append("")
        return "\n".join(lines).strip() + "\n"
