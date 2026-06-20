from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from statistics import mean


@dataclass(frozen=True)
class SynergyNode:
    name: str
    family: str
    usefulness: float
    proof: float
    leverage: float
    safety: float
    novelty: float


@dataclass(frozen=True)
class SynergyEdge:
    names: tuple[str, ...]
    score: float
    next_action: str


class TFUGAHyperSynergy:
    def nodes(self) -> tuple[SynergyNode, ...]:
        return (
            SynergyNode("JKD-ZERO-TOUCH-Pact", "operator", 9.5, 9.1, 9.5, 9.0, 8.8),
            SynergyNode("AIT-OmniAll^oN", "meta", 9.7, 8.7, 9.8, 8.6, 9.5),
            SynergyNode("AITMetaBlueprint", "meta", 9.0, 9.2, 9.1, 9.2, 8.9),
            SynergyNode("AITBuildQueue", "construction", 9.2, 9.0, 9.4, 9.1, 8.6),
            SynergyNode("AITUniversalReplay", "simulation", 9.0, 8.9, 9.2, 9.0, 8.7),
            SynergyNode("TFUGAHyperBest", "strategy", 9.3, 8.9, 9.4, 9.1, 9.0),
        )

    def bonus(self, group: tuple[SynergyNode, ...]) -> float:
        return min(1.0, 0.18 * (len({node.family for node in group}) - 1))

    def score(self, group: tuple[SynergyNode, ...]) -> float:
        raw = (
            mean(node.usefulness for node in group) * 0.22
            + mean(node.proof for node in group) * 0.18
            + max(node.leverage for node in group) * 0.23
            + mean(node.safety for node in group) * 0.18
            + mean(node.novelty for node in group) * 0.12
            + self.bonus(group)
        )
        return round(raw, 4)

    def edge(self, group: tuple[SynergyNode, ...]) -> SynergyEdge:
        s = self.score(group)
        action = "promote" if s >= 9.25 else "strengthen"
        return SynergyEdge(tuple(node.name for node in group), s, action)

    def top(self, order: int = 3, k: int = 5) -> tuple[SynergyEdge, ...]:
        edges = [self.edge(combo) for combo in combinations(self.nodes(), order)]
        return tuple(sorted(edges, key=lambda edge: edge.score, reverse=True)[:k])

    def markdown(self) -> str:
        lines = ["# TFUGA Hyper Synergy", "", "mode: composition_only", ""]
        for edge in self.top(3):
            lines.append(f"- `{', '.join(edge.names)}` score `{edge.score}` action `{edge.next_action}`")
        return "\n".join(lines).strip() + "\n"
