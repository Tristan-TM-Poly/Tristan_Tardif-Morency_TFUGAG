"""TFUGAG AIT OmniGenesis.

Strategic research orchestration layer for TFUGAG. OmniGenesis combines
frontiers, questions, memory polarity, evidence needs, contradiction pressure,
and web-tool plans into reviewable improvement candidates.

It does not browse the web, call external APIs, execute code, deploy systems,
self-modify, or mutate canon. It creates structured plans for review.
"""
from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

from src.tfuga_omega_memory_polarity import OmegaMemoryRecord, MemoryPolarity
from src.tfuga_omega_question_engine import OmegaQuestion

class OmniGenesisCandidateType(str, Enum):
    VALIDATION = "validation"
    REFUTATION = "refutation"
    IMPROVEMENT = "improvement"
    BRIDGE = "bridge"
    APPLICATION = "application"
    WEB_RESEARCH = "web_research"

@dataclass(frozen=True)
class OmniGenesisInput:
    focus_node_id: str
    focus_title: str
    questions: list[OmegaQuestion]
    memory_records: list[OmegaMemoryRecord]
    source_domains: list[str]

@dataclass(frozen=True)
class OmniGenesisCandidate:
    candidate_id: str
    focus_node_id: str
    candidate_type: OmniGenesisCandidateType
    objective: str
    use_positive_memory: list[str]
    avoid_negative_memory: list[str]
    suggested_sources: list[str]
    expected_outputs: list[str]
    review_route: str
    priority: float


def _memory_split(records: list[OmegaMemoryRecord]) -> tuple[list[str], list[str]]:
    positive = []
    negative = []
    for record in records:
        if record.polarity == MemoryPolarity.POSITIVE:
            positive.append(record.lesson)
        else:
            negative.append(record.lesson)
    return positive, negative


def generate_omnigenesis_candidates(payload: OmniGenesisInput) -> list[OmniGenesisCandidate]:
    positive, negative = _memory_split(payload.memory_records)
    candidates = []
    for index, question in enumerate(payload.questions):
        if question.question_type == "evidence_gap":
            ctype = OmniGenesisCandidateType.VALIDATION
            route = "WebResearchPlan -> EvidenceGraph -> OmegaPromotion"
            outputs = ["source shortlist", "evidence candidates", "confidence update"]
        elif question.question_type == "contradiction_resolution":
            ctype = OmniGenesisCandidateType.REFUTATION
            route = "ContradictionReview -> NegativeMemory -> OmegaEvolution"
            outputs = ["counterexample search plan", "conflict packet", "quarantine recommendation"]
        elif question.question_type == "bridge_gap":
            ctype = OmniGenesisCandidateType.BRIDGE
            route = "BridgeCandidate -> EvidenceCheck -> AtlasUpdate"
            outputs = ["bridge candidate", "analogy rationale", "risk flags"]
        elif question.question_type == "protocol_candidate":
            ctype = OmniGenesisCandidateType.IMPROVEMENT
            route = "OmegaProtocol -> EvidenceGraph -> OmegaEvolution"
            outputs = ["protocol candidate", "success criteria", "refutation criteria"]
        else:
            ctype = OmniGenesisCandidateType.WEB_RESEARCH
            route = "WebIngestionPlanner -> OmegaQuestion -> OmegaResearchPlanner"
            outputs = ["research map", "source domains", "new questions"]

        candidates.append(OmniGenesisCandidate(
            candidate_id=f"omnigenesis_{payload.focus_node_id}_{index}",
            focus_node_id=payload.focus_node_id,
            candidate_type=ctype,
            objective=f"Improve {payload.focus_title}: {question.question}",
            use_positive_memory=positive[:5],
            avoid_negative_memory=negative[:5],
            suggested_sources=payload.source_domains,
            expected_outputs=outputs,
            review_route=route,
            priority=question.priority,
        ))
    return sorted(candidates, key=lambda candidate: candidate.priority, reverse=True)


def write_omnigenesis_candidates(candidates: list[OmniGenesisCandidate], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(candidate) for candidate in candidates], indent=2, ensure_ascii=False), encoding="utf-8")
    return path
