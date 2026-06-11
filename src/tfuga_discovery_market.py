"""TFUGAG Discovery Market.

Assigns value signals to questions, experiments, bridges and claims.
Used by the Research Planner to prioritize discovery effort.
"""
from dataclasses import dataclass, asdict
import json
from pathlib import Path

@dataclass(frozen=True)
class DiscoveryCandidate:
    candidate_id:str
    category:str
    novelty:int
    scientific_value:int
    engineering_value:int
    strategic_value:int
    reusability:int

@dataclass(frozen=True)
class DiscoveryValuation:
    candidate_id:str
    score:float
    tier:str


def evaluate(candidate:DiscoveryCandidate)->DiscoveryValuation:
    score=(candidate.novelty*2 + candidate.scientific_value + candidate.engineering_value + candidate.strategic_value + candidate.reusability)
    if score>=40:
        tier='omega'
    elif score>=25:
        tier='alpha'
    elif score>=12:
        tier='beta'
    else:
        tier='gamma'
    return DiscoveryValuation(candidate.candidate_id,float(score),tier)


def write_market_snapshot(valuations, output_path):
    path=Path(output_path)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps([asdict(v) for v in valuations],indent=2),encoding='utf-8')
    return path
