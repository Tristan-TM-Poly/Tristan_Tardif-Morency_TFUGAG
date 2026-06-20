"""Meta-Evolution Engine for TFUGAG.

Measures which rules, experiments, bridges, and governance decisions generate
the most useful outcomes. Produces learning signals about the research process
itself.
"""
from dataclasses import dataclass, asdict
import json
from pathlib import Path

@dataclass(frozen=True)
class ProcessOutcome:
    source_id: str
    category: str
    discoveries_generated: int
    contradictions_found: int
    experiments_completed: int
    canon_promotions: int

@dataclass(frozen=True)
class MetaEvolutionReport:
    source_id: str
    effectiveness_score: float
    recommendation: str


def evaluate_outcome(outcome: ProcessOutcome) -> MetaEvolutionReport:
    score = (
        outcome.discoveries_generated * 3
        + outcome.experiments_completed * 2
        + outcome.canon_promotions * 5
        - outcome.contradictions_found
    )

    if score >= 20:
        rec = "amplify"
    elif score >= 5:
        rec = "maintain"
    else:
        rec = "review"

    return MetaEvolutionReport(outcome.source_id, float(score), rec)


def write_meta_evolution_report(reports, output_path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(r) for r in reports], indent=2), encoding='utf-8')
    return path
