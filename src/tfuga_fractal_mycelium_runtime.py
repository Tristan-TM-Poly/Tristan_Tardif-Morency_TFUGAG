"""TFUGAG Fractal Mycelium Runtime.

Combines fractal atlas expansion with discovery valuation and a simple budget.
It creates bounded, reviewable growth plans around a focus node instead of
letting combinatorics explode.
"""
from dataclasses import dataclass, asdict
import json
from pathlib import Path

from src.tfuga_discovery_market import DiscoveryCandidate, evaluate
from src.tfuga_fractal_atlas_engine import LENSES

@dataclass(frozen=True)
class MyceliumBudget:
    max_children: int = 8
    min_score: float = 12.0

@dataclass(frozen=True)
class MyceliumBranch:
    branch_id: str
    lens: str
    valuation_score: float
    tier: str
    next_action: str

@dataclass(frozen=True)
class MyceliumExpansion:
    focus_id: str
    title: str
    branches: list[MyceliumBranch]


def candidate_for_lens(focus_id: str, lens: str) -> DiscoveryCandidate:
    base = {
        "sources": (4, 4, 3, 3, 5),
        "claims": (5, 5, 4, 4, 5),
        "questions": (5, 5, 5, 5, 5),
        "experiments": (4, 5, 5, 5, 4),
        "applications": (4, 3, 5, 5, 4),
        "risks": (3, 4, 4, 5, 5),
        "contradictions": (5, 5, 4, 5, 5),
        "bridges": (5, 5, 5, 5, 5),
    }.get(lens, (3, 3, 3, 3, 3))
    return DiscoveryCandidate(f"{focus_id}.{lens}", lens, *base)


def expand_mycelium(focus_id: str, title: str, budget: MyceliumBudget = MyceliumBudget()) -> MyceliumExpansion:
    branches = []
    for lens in LENSES:
        valuation = evaluate(candidate_for_lens(focus_id, lens))
        if valuation.score >= budget.min_score:
            branches.append(MyceliumBranch(
                branch_id=f"{focus_id}.{lens}",
                lens=lens,
                valuation_score=valuation.score,
                tier=valuation.tier,
                next_action=f"Generate review packet for {lens} around {title}.",
            ))
    branches = sorted(branches, key=lambda b: b.valuation_score, reverse=True)[:budget.max_children]
    return MyceliumExpansion(focus_id, title, branches)


def write_mycelium_expansion(expansion: MyceliumExpansion, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(expansion), indent=2, ensure_ascii=False), encoding="utf-8")
    return path
