from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CVCDWeights:
    coherence: float = 0.25
    value: float = 0.20
    compression: float = 0.15
    density: float = 0.15
    proofability: float = 0.15
    yield_potential: float = 0.10
    error_penalty: float = 0.20


class CVCDScorer:
    """Simple CVCD+ scorer.

    CVCD+ = coherence + value + compression + density + proofability + yield
    minus explicit residue/error pressure.
    """

    def __init__(self, weights: CVCDWeights | None = None) -> None:
        self.weights = weights or CVCDWeights()

    def score(self, hgfm: dict[str, Any]) -> float:
        nodes = hgfm.get("nodes", [])
        edges = hgfm.get("hyperedges", [])
        residues = hgfm.get("residues", [])
        validators = [n for n in nodes if n.get("kind") == "validator"]
        outputs = [n for n in nodes if n.get("kind") == "output"]
        yields = [n for n in nodes if n.get("kind") == "yield"]

        coherence = min(1.0, len(edges) / max(1, len(nodes)))
        value = min(1.0, len(outputs) / 4)
        compression = 1.0 / max(1.0, len(nodes) / 12)
        density = min(1.0, len(edges) / max(1, len(nodes) - 1))
        proofability = min(1.0, len(validators) / 3)
        yield_potential = min(1.0, len(yields) / 3)
        error_pressure = min(1.0, len(residues) / 5)

        w = self.weights
        score = (
            w.coherence * coherence
            + w.value * value
            + w.compression * compression
            + w.density * density
            + w.proofability * proofability
            + w.yield_potential * yield_potential
            - w.error_penalty * error_pressure
        )
        return round(max(0.0, min(1.0, score)), 4)
