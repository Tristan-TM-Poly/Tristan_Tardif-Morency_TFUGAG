"""Meta-Governance Engine for TFUGAG.

Evaluates governance rules themselves: promotion rules, OAK rules, main
validation rules, bridge rules, and experiment rules. It emits governance review
packets only; it does not rewrite policy or mutate main.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path


class GovernanceDomain(str, Enum):
    PROMOTION = "promotion"
    OAK = "oak"
    MAIN_VALIDATION = "main_validation"
    BRIDGE = "bridge"
    CONTRADICTION = "contradiction"
    EXPERIMENT = "experiment"
    ATLAS = "atlas"


class GovernanceDecision(str, Enum):
    KEEP = "keep"
    REVIEW = "review"
    TIGHTEN = "tighten"
    RELAX = "relax"
    SPLIT = "split"
    ARCHIVE = "archive"


@dataclass(frozen=True)
class GovernanceRule:
    rule_id: str
    domain: GovernanceDomain
    statement: str
    purpose: str
    failure_modes: list[str]
    evidence_refs: list[str]


@dataclass(frozen=True)
class GovernanceReviewPacket:
    rule_id: str
    decision: GovernanceDecision
    score: int
    rationale: list[str]
    recommended_next_action: str


def evaluate_rule(rule: GovernanceRule) -> GovernanceReviewPacket:
    score = 0
    rationale: list[str] = []

    if rule.statement.strip():
        score += 25
        rationale.append("rule statement present")
    else:
        rationale.append("missing rule statement")

    if rule.purpose.strip():
        score += 25
        rationale.append("purpose present")
    else:
        rationale.append("missing purpose")

    if rule.failure_modes:
        score += 25
        rationale.append("failure modes listed")
    else:
        rationale.append("failure modes missing")

    if rule.evidence_refs:
        score += 25
        rationale.append("evidence references present")
    else:
        rationale.append("evidence references missing")

    if score >= 90:
        decision = GovernanceDecision.KEEP
        action = "Keep rule; re-evaluate after future incidents or contradictions."
    elif score >= 65:
        decision = GovernanceDecision.REVIEW
        action = "Review rule before relying on it for canon decisions."
    elif not rule.failure_modes:
        decision = GovernanceDecision.TIGHTEN
        action = "Add failure modes and guardrails."
    elif not rule.purpose.strip():
        decision = GovernanceDecision.SPLIT
        action = "Split vague rule into smaller purpose-specific rules."
    else:
        decision = GovernanceDecision.REVIEW
        action = "Add missing evidence and clarify scope."

    return GovernanceReviewPacket(rule.rule_id, decision, score, rationale, action)


def evaluate_rules(rules: list[GovernanceRule]) -> list[GovernanceReviewPacket]:
    return sorted([evaluate_rule(rule) for rule in rules], key=lambda packet: packet.score)


def write_governance_review(packets: list[GovernanceReviewPacket], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(packet) for packet in packets], indent=2, ensure_ascii=False), encoding="utf-8")
    return path
