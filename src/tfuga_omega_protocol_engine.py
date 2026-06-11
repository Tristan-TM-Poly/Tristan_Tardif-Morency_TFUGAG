"""TFUGAG Omega Protocol Engine.

Transforms OmegaResearchCandidate objects into descriptive protocol candidates.
This module does not run protocols, execute code, access external systems,
or mutate canon. It only creates reviewable protocol specifications.
"""
from dataclasses import dataclass, asdict
import json
from pathlib import Path

from src.tfuga_omega_research_planner import OmegaResearchCandidate

@dataclass(frozen=True)
class OmegaProtocolCandidate:
    protocol_id: str
    source_candidate_id: str
    node_id: str
    hypothesis: str
    variables: list[str]
    success_criteria: list[str]
    refutation_criteria: list[str]
    expected_artifacts: list[str]
    review_route: str
    priority: float


def protocol_from_candidate(candidate: OmegaResearchCandidate) -> OmegaProtocolCandidate:
    objective = candidate.objective
    route = candidate.validation_route

    if "Evidence" in route:
        variables = ["claim", "source", "evidence relation", "confidence"]
        success = ["evidence object created", "relation to claim declared", "confidence updated"]
        refute = ["source is irrelevant", "evidence contradicts claim", "confidence cannot be justified"]
    elif "Bridge" in route:
        variables = ["source node", "target node", "relation type", "rationale"]
        success = ["bridge relation specified", "analogy or dependency justified", "review packet generated"]
        refute = ["bridge is superficial", "domains are incompatible", "contradiction pressure rises"]
    elif "Quarantine" in route or "OAK" in route:
        variables = ["conflict claim", "assumptions", "evidence refs", "resolution note"]
        success = ["conflict localized", "assumptions separated", "resolution path proposed"]
        refute = ["conflict cannot be localized", "evidence remains ambiguous", "claims require archival"]
    elif "Protocol" in route:
        variables = ["objective", "inputs", "outputs", "constraints"]
        success = ["protocol record created", "expected outputs listed", "evidence mapping prepared"]
        refute = ["objective too vague", "outputs not measurable", "constraints missing"]
    else:
        variables = ["focus node", "atlas lens", "linked nodes"]
        success = ["atlas view created", "frontier refs attached", "question refs attached"]
        refute = ["view lacks linked nodes", "frontiers absent", "no useful navigation produced"]

    return OmegaProtocolCandidate(
        protocol_id=f"proto_{candidate.candidate_id}",
        source_candidate_id=candidate.candidate_id,
        node_id=candidate.node_id,
        hypothesis=f"Resolving this candidate will reduce uncertainty: {objective}",
        variables=variables,
        success_criteria=success,
        refutation_criteria=refute,
        expected_artifacts=candidate.expected_deliverables,
        review_route=route,
        priority=candidate.priority,
    )


def protocols_from_candidates(candidates: list[OmegaResearchCandidate]) -> list[OmegaProtocolCandidate]:
    return sorted([protocol_from_candidate(candidate) for candidate in candidates], key=lambda p: p.priority, reverse=True)


def write_omega_protocols(protocols: list[OmegaProtocolCandidate], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(protocol) for protocol in protocols], indent=2, ensure_ascii=False), encoding="utf-8")
    return path
