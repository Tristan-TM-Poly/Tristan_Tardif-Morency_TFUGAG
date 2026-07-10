"""TFUGAG Model Interaction Bus.

Coordinates multiple AI model providers as proposal generators. Models do not
mutate the repository, main branch, canon, or external systems. They emit
structured proposals that TFUGAG can compare, score, quarantine, and review.
"""
from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

class ModelRole(str, Enum):
    GENERATOR = "generator"
    CRITIC = "critic"
    VERIFIER = "verifier"
    SYNTHESIZER = "synthesizer"

class InteractionDecision(str, Enum):
    ACCEPT_FOR_REVIEW = "accept_for_review"
    NEEDS_MORE_EVIDENCE = "needs_more_evidence"
    CONFLICT = "conflict"
    REJECT = "reject"

@dataclass(frozen=True)
class ModelEndpoint:
    name: str
    provider: str
    role: ModelRole
    secret_env_var: str
    enabled: bool = True

@dataclass(frozen=True)
class ModelProposal:
    model_name: str
    role: ModelRole
    task_id: str
    claim: str
    rationale: str
    evidence_refs: list[str]
    limitations: list[str]
    confidence: float

@dataclass(frozen=True)
class InteractionPacket:
    task_id: str
    proposals: list[ModelProposal]
    decision: InteractionDecision
    rationale: list[str]

DEFAULT_ENDPOINTS = [
    ModelEndpoint("gemini_primary", "google", ModelRole.GENERATOR, "GEMINI_API_KEY"),
    ModelEndpoint("chatgpt_critic", "openai", ModelRole.CRITIC, "OPENAI_API_KEY"),
    ModelEndpoint("local_verifier", "local", ModelRole.VERIFIER, ""),
]

def score_proposal(proposal: ModelProposal) -> float:
    evidence_score = min(1.0, len(proposal.evidence_refs) / 3)
    limitation_score = min(1.0, len(proposal.limitations) / 3)
    return (proposal.confidence * 0.5) + (evidence_score * 0.3) + (limitation_score * 0.2)


def arbitrate(task_id: str, proposals: list[ModelProposal]) -> InteractionPacket:
    if not proposals:
        return InteractionPacket(task_id, [], InteractionDecision.REJECT, ["no proposals"])

    scores = [score_proposal(p) for p in proposals]
    avg = sum(scores) / len(scores)
    rationales = [f"{p.model_name}:{score_proposal(p):.2f}" for p in proposals]

    claims = {p.claim.strip().lower() for p in proposals if p.claim.strip()}
    if len(claims) > 1:
        return InteractionPacket(task_id, proposals, InteractionDecision.CONFLICT, rationales + ["models disagree"])
    if avg >= 0.75:
        return InteractionPacket(task_id, proposals, InteractionDecision.ACCEPT_FOR_REVIEW, rationales)
    if avg >= 0.45:
        return InteractionPacket(task_id, proposals, InteractionDecision.NEEDS_MORE_EVIDENCE, rationales)
    return InteractionPacket(task_id, proposals, InteractionDecision.REJECT, rationales)


def write_interaction_packet(packet: InteractionPacket, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(packet), indent=2, ensure_ascii=False), encoding="utf-8")
    return path
