"""Self-proposal engine for TFUGAG.

The system does not mutate itself here. It inspects review artifacts and emits
bounded proposals that can be reviewed by OAK and staged through a pull request.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

from src.tfuga_airgap import KnowledgeAtom
from src.tfuga_agent_bridge import ActionType, AgentAction
from src.tfuga_bridge_engine import BridgeCandidate, propose_bridges
from src.tfuga_contradiction_engine import ContradictionCandidate, propose_contradictions


class ProposalKind(str, Enum):
    ADD_BRIDGE = "add_bridge"
    REVIEW_CONTRADICTION = "review_contradiction"
    ADD_EVIDENCE = "add_evidence"
    ADD_LIMITATION = "add_limitation"
    DOWNGRADE_STATUS = "downgrade_status"


@dataclass(frozen=True)
class SystemProposal:
    kind: ProposalKind
    title: str
    rationale: str
    priority: int
    action: AgentAction

    def to_dict(self) -> dict:
        data = asdict(self)
        data["kind"] = self.kind.value
        return data


def proposal_from_bridge(candidate: BridgeCandidate) -> SystemProposal:
    content = json.dumps(candidate.to_dict(), indent=2, ensure_ascii=False)
    return SystemProposal(
        kind=ProposalKind.ADD_BRIDGE,
        title=f"Review bridge {candidate.source_id} -> {candidate.target_id}",
        rationale=candidate.rationale,
        priority=50 + int(candidate.score * 50),
        action=AgentAction(
            action_type=ActionType.OPEN_REVIEW,
            title="Review bridge candidate",
            rationale=candidate.rationale,
            target_path=f"reviews/bridges/{candidate.source_id}__{candidate.target_id}.json",
            content=content,
        ),
    )


def proposal_from_contradiction(candidate: ContradictionCandidate) -> SystemProposal:
    content = json.dumps(candidate.to_dict(), indent=2, ensure_ascii=False)
    return SystemProposal(
        kind=ProposalKind.REVIEW_CONTRADICTION,
        title=f"Review contradiction {candidate.left_id} vs {candidate.right_id}",
        rationale=candidate.rationale,
        priority=90 + int(candidate.score * 10),
        action=AgentAction(
            action_type=ActionType.OPEN_REVIEW,
            title="Review contradiction candidate",
            rationale=candidate.rationale,
            target_path=f"reviews/contradictions/{candidate.left_id}__{candidate.right_id}.json",
            content=content,
        ),
    )


def proposals_from_atoms(atoms: dict[str, KnowledgeAtom]) -> list[SystemProposal]:
    proposals: list[SystemProposal] = []
    for bridge in propose_bridges(atoms):
        proposals.append(proposal_from_bridge(bridge))
    for contradiction in propose_contradictions(atoms):
        proposals.append(proposal_from_contradiction(contradiction))
    for atom_id, atom in atoms.items():
        if not atom.evidence and atom.status.value in {"D", "C"}:
            proposals.append(
                SystemProposal(
                    kind=ProposalKind.ADD_EVIDENCE,
                    title=f"Add evidence for {atom_id}",
                    rationale="Promoted atoms require evidence before they can remain promoted.",
                    priority=85,
                    action=AgentAction(
                        action_type=ActionType.OPEN_REVIEW,
                        title="Review missing evidence",
                        rationale="Promoted atom lacks evidence.",
                        target_path=f"reviews/evidence/{atom_id}.json",
                        content=json.dumps({"atom_id": atom_id, "issue": "missing_evidence"}, indent=2),
                    ),
                )
            )
        if not atom.limitations:
            proposals.append(
                SystemProposal(
                    kind=ProposalKind.ADD_LIMITATION,
                    title=f"Add limitations for {atom_id}",
                    rationale="Atoms need limitations before promotion or reuse.",
                    priority=70,
                    action=AgentAction(
                        action_type=ActionType.OPEN_REVIEW,
                        title="Review missing limitations",
                        rationale="Atom lacks limitations.",
                        target_path=f"reviews/limitations/{atom_id}.json",
                        content=json.dumps({"atom_id": atom_id, "issue": "missing_limitations"}, indent=2),
                    ),
                )
            )
    return sorted(proposals, key=lambda item: item.priority, reverse=True)


def write_proposals(proposals: list[SystemProposal], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([proposal.to_dict() for proposal in proposals], indent=2, ensure_ascii=False), encoding="utf-8")
    return path
