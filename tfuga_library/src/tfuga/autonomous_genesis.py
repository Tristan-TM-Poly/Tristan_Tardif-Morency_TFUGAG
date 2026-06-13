from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class GenesisSeed:
    name: str
    purpose: str
    source: str
    expected_gain: float
    risk: str = "low"


@dataclass(frozen=True)
class GenesisProposal:
    title: str
    oak_score: float
    rationale: str
    actions: tuple[str, ...]
    gates: tuple[str, ...]


@dataclass(frozen=True)
class GenesisReport:
    proposals: tuple[GenesisProposal, ...]
    accepted: tuple[GenesisProposal, ...]
    rejected: tuple[GenesisProposal, ...]
    markdown: str


@dataclass(frozen=True)
class GenesisPolicy:
    min_oak_score: float = 6.0
    allow_high_risk: bool = False
    require_tests: bool = True
    require_docs: bool = True
    require_draft_pr: bool = True


class AITAutonomousGenesis:
    """Bounded OAK-gated proposal generator for TFUGA."""

    def __init__(self, policy: GenesisPolicy | None = None) -> None:
        self.policy = policy or GenesisPolicy()

    def propose(self, seed: GenesisSeed) -> GenesisProposal:
        risk_penalty = {"low": 0.0, "medium": 1.0, "high": 3.0}.get(seed.risk, 2.0)
        score = max(0.0, min(10.0, 5.0 + seed.expected_gain - risk_penalty))
        actions = [
            f"create module for {seed.name}",
            "add tests",
            "add docs",
            "add OAK memory entry",
            "open or update draft PR",
        ]
        gates = ["oak_score", "tests", "docs", "review"]
        if self.policy.require_draft_pr:
            gates.append("draft_pr")
        rationale = f"{seed.purpose} from {seed.source}; expected gain {seed.expected_gain}; risk {seed.risk}."
        return GenesisProposal(seed.name, round(score, 3), rationale, tuple(actions), tuple(gates))

    def generate(self, seeds: Iterable[GenesisSeed]) -> GenesisReport:
        proposals = tuple(self.propose(seed) for seed in seeds)
        accepted: list[GenesisProposal] = []
        rejected: list[GenesisProposal] = []
        for proposal in proposals:
            high_risk = "risk high" in proposal.rationale
            if proposal.oak_score >= self.policy.min_oak_score and (self.policy.allow_high_risk or not high_risk):
                accepted.append(proposal)
            else:
                rejected.append(proposal)
        markdown = self.markdown_report(proposals, tuple(accepted), tuple(rejected))
        return GenesisReport(proposals, tuple(accepted), tuple(rejected), markdown)

    def markdown_report(self, proposals: tuple[GenesisProposal, ...], accepted: tuple[GenesisProposal, ...], rejected: tuple[GenesisProposal, ...]) -> str:
        lines = ["# AIT Autonomous Genesis Report", ""]
        lines.append(f"Total proposals: `{len(proposals)}`")
        lines.append(f"Accepted: `{len(accepted)}`")
        lines.append(f"Rejected: `{len(rejected)}`")
        lines.extend(["", "## Accepted", ""])
        for item in accepted:
            lines.append(f"### {item.title}")
            lines.append(f"- OAK score: `{item.oak_score}`")
            lines.append(f"- rationale: {item.rationale}")
            for action in item.actions:
                lines.append(f"- [ ] {action}")
            lines.append("")
        lines.extend(["## Rejected", ""])
        for item in rejected:
            lines.append(f"- `{item.title}` — score `{item.oak_score}` — {item.rationale}")
        return "\n".join(lines).strip() + "\n"

    def default_seeds(self) -> tuple[GenesisSeed, ...]:
        return (
            GenesisSeed("AIT repo analyzer loop", "analyze repos and generate improvement proposals", "tfuga PR6", 4.0, "low"),
            GenesisSeed("AIT capability adapter loop", "map external capabilities into safe adapters", "capability cards", 3.5, "low"),
            GenesisSeed("AIT delivery gate loop", "estimate hidden work and required merge gates", "delivery harness", 3.0, "low"),
        )
