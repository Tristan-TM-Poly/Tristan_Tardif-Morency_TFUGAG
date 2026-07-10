"""Main Agent Validator for TFUGAG.

Agents that guard main may validate proposed changes autonomously, but this
module only emits a decision packet. It does not merge, push, deploy, or mutate
main. A repository policy may use this packet as a required review signal.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path


class MainValidationDecision(str, Enum):
    APPROVE_FOR_REVIEW = "approve_for_review"
    BLOCK = "block"
    NEEDS_TESTS = "needs_tests"
    NEEDS_OAK_REVIEW = "needs_oak_review"
    NEEDS_ROLLBACK_PLAN = "needs_rollback_plan"


@dataclass(frozen=True)
class MainUpdateProposal:
    source_branch: str
    target_branch: str
    changed_modules: list[str]
    tests_present: bool
    oak_review_present: bool
    rollback_plan_present: bool
    risk_flags: list[str]


@dataclass(frozen=True)
class MainValidationPacket:
    proposal: MainUpdateProposal
    decision: MainValidationDecision
    score: int
    rationale: list[str]


def validate_main_update(proposal: MainUpdateProposal) -> MainValidationPacket:
    score = 0
    rationale: list[str] = []

    if proposal.target_branch != "main":
        return MainValidationPacket(proposal, MainValidationDecision.BLOCK, 0, ["target branch must be main"])
    if not proposal.changed_modules:
        return MainValidationPacket(proposal, MainValidationDecision.BLOCK, 0, ["no changed modules listed"])

    score += min(30, len(proposal.changed_modules) * 5)
    rationale.append("changed modules listed")

    if proposal.tests_present:
        score += 25
        rationale.append("tests present")
    else:
        rationale.append("tests missing")

    if proposal.oak_review_present:
        score += 25
        rationale.append("OAK review present")
    else:
        rationale.append("OAK review missing")

    if proposal.rollback_plan_present:
        score += 10
        rationale.append("rollback plan present")
    else:
        rationale.append("rollback plan missing")

    if not proposal.risk_flags:
        score += 10
        rationale.append("no risk flags declared")
    else:
        rationale.append("risk flags require review")

    if not proposal.tests_present:
        decision = MainValidationDecision.NEEDS_TESTS
    elif not proposal.oak_review_present:
        decision = MainValidationDecision.NEEDS_OAK_REVIEW
    elif not proposal.rollback_plan_present:
        decision = MainValidationDecision.NEEDS_ROLLBACK_PLAN
    elif proposal.risk_flags:
        decision = MainValidationDecision.NEEDS_OAK_REVIEW
    else:
        decision = MainValidationDecision.APPROVE_FOR_REVIEW

    return MainValidationPacket(proposal, decision, score, rationale)


def write_main_validation_packet(packet: MainValidationPacket, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(packet), indent=2, ensure_ascii=False), encoding="utf-8")
    return path
