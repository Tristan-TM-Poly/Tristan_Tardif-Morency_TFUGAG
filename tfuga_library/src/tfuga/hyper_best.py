from __future__ import annotations

from dataclasses import dataclass
from statistics import mean


@dataclass(frozen=True)
class HyperMove:
    name: str
    layer: str
    usefulness: float
    proof: float
    leverage: float
    safety: float
    recognition: float
    cost: float = 1.0


@dataclass(frozen=True)
class HyperScore:
    name: str
    score: float
    oak_level: float
    next_action: str


class TFUGAHyperBest:
    def moves(self) -> tuple[HyperMove, ...]:
        return (
            HyperMove("JKD-ZERO-TOUCH-Pact", "operator", 9.5, 9.1, 9.5, 9.0, 9.3, 0.8),
            HyperMove("AITMetaBlueprint", "meta", 9.0, 9.2, 9.1, 9.2, 8.4, 0.9),
            HyperMove("AITBuildQueue", "meta", 9.2, 9.0, 9.4, 9.1, 8.2, 1.0),
            HyperMove("AITUniversalReplay", "simulation", 9.0, 8.9, 9.2, 9.0, 8.7, 1.0),
            HyperMove("AITReleaseQueue", "publication", 8.7, 8.2, 8.8, 9.2, 9.1, 1.0),
            HyperMove("AIT-OmniAll^oN", "meta", 9.7, 8.7, 9.8, 8.6, 9.5, 1.2),
        )

    def score(self, move: HyperMove) -> HyperScore:
        value = (
            move.usefulness * 0.24
            + move.proof * 0.22
            + move.leverage * 0.24
            + move.safety * 0.18
            + move.recognition * 0.12
        ) / max(move.cost, 0.1)
        oak = mean((move.proof, move.safety, min(10.0, value)))
        action = "promote" if oak >= 9.0 else "strengthen"
        return HyperScore(move.name, round(value, 4), round(oak, 4), action)

    def rank(self) -> tuple[HyperScore, ...]:
        return tuple(sorted((self.score(move) for move in self.moves()), key=lambda item: item.score, reverse=True))

    def markdown(self) -> str:
        lines = ["# TFUGA HyperBest", "", "mode: composition_only", ""]
        for item in self.rank():
            lines.append(f"- `{item.name}` score `{item.score}` oak `{item.oak_level}` action `{item.next_action}`")
        return "\n".join(lines).strip() + "\n"
