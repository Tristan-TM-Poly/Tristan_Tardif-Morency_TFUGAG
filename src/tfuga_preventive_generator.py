"""Preventive subgraph generator for TFUGAG.

When a theory, system, application, or creation is inspected, this module emits
reviewable proposals around that focus. It does not mutate the repository. It
creates candidate expansions for hypergraph-style exploration.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

from src.tfuga_airgap import KnowledgeAtom
from src.tfuga_proposal_engine import SystemProposal, ProposalKind
from src.tfuga_agent_bridge import ActionType, AgentAction


class FocusType(str, Enum):
    THEORY = "theory"
    SYSTEM = "system"
    APPLICATION = "application"
    CREATION = "creation"


class PreventiveLens(str, Enum):
    DEFINITIONS = "definitions"
    EVIDENCE = "evidence"
    LIMITATIONS = "limitations"
    BRIDGES = "bridges"
    CONTRADICTIONS = "contradictions"
    EXPERIMENTS = "experiments"
    APPLICATIONS = "applications"
    RISKS = "risks"


@dataclass(frozen=True)
class ZoomFocus:
    focus_id: str
    title: str
    focus_type: FocusType
    description: str


@dataclass(frozen=True)
class PreventiveSubgraphSeed:
    focus: ZoomFocus
    lens: PreventiveLens
    proposal_title: str
    rationale: str
    target_path: str
    payload: dict

    def to_proposal(self, priority: int = 60) -> SystemProposal:
        return SystemProposal(
            kind=ProposalKind.ADD_LIMITATION if self.lens in {PreventiveLens.LIMITATIONS, PreventiveLens.RISKS} else ProposalKind.ADD_EVIDENCE,
            title=self.proposal_title,
            rationale=self.rationale,
            priority=priority,
            action=AgentAction(
                action_type=ActionType.OPEN_REVIEW,
                title=self.proposal_title,
                rationale=self.rationale,
                target_path=self.target_path,
                content=json.dumps(self.payload, indent=2, ensure_ascii=False),
            ),
        )


def safe_slug(text: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in text).strip("_")[:80] or "focus"


def generate_preventive_seeds(focus: ZoomFocus) -> list[PreventiveSubgraphSeed]:
    base = safe_slug(focus.focus_id or focus.title)
    seeds: list[PreventiveSubgraphSeed] = []
    templates = [
        (PreventiveLens.DEFINITIONS, "Define minimal objects", "Clarify the smallest definitions required for this focus."),
        (PreventiveLens.EVIDENCE, "List evidence requirements", "Identify what would be needed to support or falsify this focus."),
        (PreventiveLens.LIMITATIONS, "List boundary conditions", "Prevent overextension by naming limits and failure modes."),
        (PreventiveLens.BRIDGES, "Suggest neighboring domains", "Prepare candidate bridges to adjacent theories, systems, applications, or creations."),
        (PreventiveLens.CONTRADICTIONS, "Search for conflict surfaces", "Identify likely contradiction zones before canon promotion."),
        (PreventiveLens.EXPERIMENTS, "Propose smallest experiments", "Turn the focus into testable or executable next steps."),
        (PreventiveLens.APPLICATIONS, "Map application surfaces", "Find possible use cases without claiming deployment readiness."),
        (PreventiveLens.RISKS, "Prepare OAK risk review", "List conceptual, technical, ethical, and operational risks."),
    ]
    for lens, title, rationale in templates:
        target_path = f"reviews/preventive/{base}/{lens.value}.json"
        payload = {
            "focus": asdict(focus),
            "lens": lens.value,
            "review_questions": review_questions_for_lens(lens),
            "status": "candidate_subgraph_seed",
        }
        seeds.append(
            PreventiveSubgraphSeed(
                focus=focus,
                lens=lens,
                proposal_title=f"{title}: {focus.title}",
                rationale=rationale,
                target_path=target_path,
                payload=payload,
            )
        )
    return seeds


def review_questions_for_lens(lens: PreventiveLens) -> list[str]:
    questions = {
        PreventiveLens.DEFINITIONS: [
            "What are the primitive objects?",
            "What must be excluded from the definition?",
            "What notation is required?",
        ],
        PreventiveLens.EVIDENCE: [
            "What evidence would support this?",
            "What observation would falsify this?",
            "What is the weakest acceptable demonstration?",
        ],
        PreventiveLens.LIMITATIONS: [
            "Where does this likely fail?",
            "What assumptions are fragile?",
            "What should not be claimed yet?",
        ],
        PreventiveLens.BRIDGES: [
            "Which domains share structure with this focus?",
            "Which analogy is useful but dangerous?",
            "What relation type should be proposed?",
        ],
        PreventiveLens.CONTRADICTIONS: [
            "Which existing claims might conflict?",
            "What negation pattern should be searched?",
            "What arbitration evidence is needed?",
        ],
        PreventiveLens.EXPERIMENTS: [
            "What is the smallest executable test?",
            "What dataset or simulation is needed?",
            "What result would upgrade the status?",
        ],
        PreventiveLens.APPLICATIONS: [
            "What use case is plausible?",
            "What user would benefit?",
            "What proof of usefulness is required?",
        ],
        PreventiveLens.RISKS: [
            "What could be overstated?",
            "What could be misused or misunderstood?",
            "What safeguard should be added?",
        ],
    }
    return questions[lens]


def proposals_for_zoom(focus: ZoomFocus) -> list[SystemProposal]:
    return [seed.to_proposal(priority=75) for seed in generate_preventive_seeds(focus)]


def atom_to_focus(atom_id: str, atom: KnowledgeAtom, focus_type: FocusType = FocusType.THEORY) -> ZoomFocus:
    return ZoomFocus(
        focus_id=atom_id,
        title=atom.title,
        focus_type=focus_type,
        description=atom.claim,
    )


def write_preventive_subgraph(focus: ZoomFocus, output_path: str | Path) -> Path:
    seeds = generate_preventive_seeds(focus)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(seed) for seed in seeds], indent=2, ensure_ascii=False), encoding="utf-8")
    return path
