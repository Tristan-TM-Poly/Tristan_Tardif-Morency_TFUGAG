from __future__ import annotations

from dataclasses import dataclass
from statistics import mean


@dataclass(frozen=True)
class OmniAtom:
    name: str
    family: str
    capability: str
    readiness: float
    risk: float = 0.0


@dataclass(frozen=True)
class OmniLayer:
    order: int
    name: str
    score: float
    risk: float
    summary: str


class AITOmniAll:
    def default_atoms(self) -> tuple[OmniAtom, ...]:
        return (
            OmniAtom("AITReadiness", "readiness", "score readiness", 8.6, 0.1),
            OmniAtom("AITBuildQueue", "meta", "queue builder plans", 9.0, 0.18),
            OmniAtom("AITMetaBlueprint", "meta", "prepare blueprints", 9.1, 0.2),
            OmniAtom("AITUniversalReplay", "replay", "simulate old tasks", 8.7, 0.23),
            OmniAtom("AITControlPlane", "control", "compose reports", 9.0, 0.16),
        )

    def compose_once(self, atoms: tuple[OmniAtom, ...], order: int) -> OmniLayer:
        if not atoms:
            raise ValueError("Need atoms.")
        score = round(mean(atom.readiness for atom in atoms), 4)
        risk = round(mean(atom.risk for atom in atoms), 4)
        return OmniLayer(order, f"AIT-OmniAll^o{order}", score, risk, f"{len(atoms)} atoms score={score} risk={risk}")

    def lift(self, layer: OmniLayer) -> OmniAtom:
        readiness = round(min(10.0, layer.score + (1.0 - layer.risk) * 0.1), 4)
        risk = round(layer.risk * 0.85, 4)
        return OmniAtom(layer.name, "omniall", layer.summary, readiness, risk)

    def circle_power(self, n: int) -> tuple[OmniLayer, ...]:
        if n < 1:
            raise ValueError("n must be >= 1")
        atoms = self.default_atoms()
        layers = []
        for order in range(1, n + 1):
            layer = self.compose_once(atoms, order)
            layers.append(layer)
            atoms = (self.lift(layer),)
        return tuple(layers)

    def markdown(self, n: int = 3) -> str:
        lines = ["# AIT OmniAll", "", "mode: composition_only", ""]
        for layer in self.circle_power(n):
            lines.append(f"- `{layer.name}` score `{layer.score}` risk `{layer.risk}`")
        return "\n".join(lines).strip() + "\n"
