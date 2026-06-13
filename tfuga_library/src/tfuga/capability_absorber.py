from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class CapabilityCard:
    """Metadata-only description of a capability to learn from."""

    name: str
    source: str
    license_name: str
    capability: str
    pattern: str
    notes: str = ""


@dataclass(frozen=True)
class CapabilityPolicy:
    """Safe absorption policy: learn patterns, do not copy code blindly."""

    allow_code_copy: bool = False
    require_license_review: bool = True
    require_adapter_boundary: bool = True
    require_tests: bool = True


@dataclass(frozen=True)
class AbsorptionPlan:
    card: CapabilityCard
    allowed: bool
    oak_score: float
    adapter_name: str
    reason: str
    next_steps: tuple[str, ...]


@dataclass(frozen=True)
class IntegrationBacklogItem:
    title: str
    priority: int
    proposal: str
    tests: tuple[str, ...] = field(default_factory=tuple)


class AITCapabilityAbsorber:
    """Map OSS/API capabilities into TFUGA adapter plans and proposals.

    Metadata-first: input cards or repository summaries, output plans, reports,
    backlogs and reviewable proposals.
    """

    permissive = {"mit", "apache-2.0", "bsd", "open-standard", "public-docs"}
    caution = {"gpl", "agpl", "lgpl", "unknown", "proprietary"}

    def __init__(self, policy: CapabilityPolicy | None = None) -> None:
        self.policy = policy or CapabilityPolicy()

    def normalize_license(self, license_name: str) -> str:
        clean = license_name.lower().replace("license", "").strip()
        if "apache" in clean:
            return "apache-2.0"
        if "mit" in clean:
            return "mit"
        if "bsd" in clean:
            return "bsd"
        if "agpl" in clean:
            return "agpl"
        if "lgpl" in clean:
            return "lgpl"
        if "gpl" in clean:
            return "gpl"
        if "standard" in clean:
            return "open-standard"
        if "doc" in clean:
            return "public-docs"
        return clean or "unknown"

    def plan(self, card: CapabilityCard) -> AbsorptionPlan:
        license_key = self.normalize_license(card.license_name)
        safe_license = license_key in self.permissive
        adapter_name = self._adapter_name(card)
        allowed = safe_license or license_key in self.caution
        score = 5.0
        if safe_license:
            score += 2.0
        else:
            score -= 1.0
        if self.policy.require_adapter_boundary:
            score += 1.0
        if self.policy.require_tests:
            score += 1.0
        if not self.policy.allow_code_copy:
            score += 1.0
        score = max(0.0, min(10.0, score))
        if safe_license:
            reason = "capability can be mapped through an adapter with attribution and tests"
        else:
            reason = "metadata-only absorption; require explicit license review before code reuse"
        steps = (
            "record source and license",
            "extract interface pattern, not raw implementation",
            f"create adapter boundary `{adapter_name}`",
            "add tests and documentation",
            "open draft PR for review",
        )
        return AbsorptionPlan(card, allowed, score, adapter_name, reason, steps)

    def plan_many(self, cards: Iterable[CapabilityCard]) -> tuple[AbsorptionPlan, ...]:
        return tuple(self.plan(card) for card in cards)

    def backlog(self, cards: Iterable[CapabilityCard]) -> tuple[IntegrationBacklogItem, ...]:
        plans = sorted(self.plan_many(cards), key=lambda p: p.oak_score, reverse=True)
        items: list[IntegrationBacklogItem] = []
        for index, plan in enumerate(plans, start=1):
            proposal = f"Integrate `{plan.card.name}` via `{plan.adapter_name}`. Rule: {plan.reason}."
            tests = (
                f"test_{plan.adapter_name}_card_is_recorded",
                f"test_{plan.adapter_name}_does_not_copy_code",
                f"test_{plan.adapter_name}_has_oak_report",
            )
            items.append(IntegrationBacklogItem(plan.card.name, index, proposal, tests))
        return tuple(items)

    def markdown_report(self, cards: Iterable[CapabilityCard], title: str = "AIT Capability Absorption Report") -> str:
        plans = self.plan_many(cards)
        lines = [f"# {title}", "", "## Policy", ""]
        lines.append(f"- copy third-party code: `{self.policy.allow_code_copy}`")
        lines.append(f"- license review required: `{self.policy.require_license_review}`")
        lines.append(f"- adapter boundary required: `{self.policy.require_adapter_boundary}`")
        lines.extend(["", "## Capability plans", ""])
        for plan in plans:
            lines.append(f"### {plan.card.name}")
            lines.append("")
            lines.append(f"- source: `{plan.card.source}`")
            lines.append(f"- license: `{plan.card.license_name}`")
            lines.append(f"- capability: {plan.card.capability}")
            lines.append(f"- pattern: `{plan.card.pattern}`")
            lines.append(f"- adapter: `{plan.adapter_name}`")
            lines.append(f"- OAK score: `{plan.oak_score}`")
            lines.append(f"- reason: {plan.reason}")
            lines.append("")
        return "\n".join(lines).strip() + "\n"

    def proposal_checklist(self, cards: Iterable[CapabilityCard]) -> str:
        lines = ["# AIT Capability Integration Checklist", ""]
        for item in self.backlog(cards):
            lines.append(f"## {item.title}")
            lines.append("")
            lines.append(f"- priority: `{item.priority}`")
            lines.append(f"- proposal: {item.proposal}")
            for test in item.tests:
                lines.append(f"- [ ] `{test}`")
            lines.append("")
        return "\n".join(lines).strip() + "\n"

    def _adapter_name(self, card: CapabilityCard) -> str:
        raw = f"{card.name}_{card.pattern}".lower()
        chars = [ch if ch.isalnum() else "_" for ch in raw]
        compact = "_".join(part for part in "".join(chars).split("_") if part)
        return compact[:80] or "capability_adapter"
