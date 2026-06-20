from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AutomationMode(str, Enum):
    PLAN_ONLY = "plan_only"
    DRY_RUN = "dry_run"
    APPROVAL_REQUIRED = "approval_required"


@dataclass(frozen=True)
class AutomationNeed:
    name: str
    trigger: str
    friction: float
    frequency: float
    risk: float
    value: float
    evidence: str


@dataclass(frozen=True)
class AutomationPlan:
    name: str
    mode: AutomationMode
    oak_score: float
    friction_drop: float
    blockers: tuple[str, ...]
    recursion_depth: int


@dataclass(frozen=True)
class AutomationWorkOrder:
    plan_name: str
    approved: bool
    reason: str
    payload: dict[str, str | float | int]


class AITAutoAutomationKernel:
    def default_needs(self) -> tuple[AutomationNeed, ...]:
        return (
            AutomationNeed("PR status verifier", "after repository write", .75, .95, .2, .9, "verify every push"),
            AutomationNeed("artifact test reporter", "after artifact build", .7, .9, .15, .85, "summarize tests/OAK"),
            AutomationNeed("module gap detector", "after ranking", .8, .8, .25, .9, "infer missing modules"),
            AutomationNeed("release handoff packet", "before release", .9, .45, .55, .95, "requires review"),
            AutomationNeed("self loop expander", "after plan", .95, .8, .85, .8, "anti-loop required"),
        )

    def oak_score(self, need: AutomationNeed, depth: int = 0) -> float:
        benefit = need.value * .4 + need.friction * .25 + need.frequency * .2
        safety = max(0, 1 - need.risk) * .15
        penalty = min(.6, depth * .2)
        return round(10 * max(0, benefit + safety - penalty), 4)

    def blockers(self, need: AutomationNeed, depth: int = 0) -> tuple[str, ...]:
        out = []
        if need.risk >= .5:
            out.append("risk requires approval")
        if depth > 1:
            out.append("recursive depth exceeds safe default")
        if "self" in need.name.lower() or "loop" in need.name.lower():
            out.append("anti-loop guard required")
        if not need.evidence:
            out.append("missing evidence")
        return tuple(out)

    def mode(self, blockers: tuple[str, ...]) -> AutomationMode:
        if not blockers:
            return AutomationMode.DRY_RUN
        if any("approval" in b or "anti-loop" in b for b in blockers):
            return AutomationMode.APPROVAL_REQUIRED
        return AutomationMode.PLAN_ONLY

    def plan(self, need: AutomationNeed, depth: int = 0) -> AutomationPlan:
        blockers = self.blockers(need, depth)
        mode = self.mode(blockers)
        drop = round(need.friction * (.75 if mode == AutomationMode.DRY_RUN else .35), 4)
        return AutomationPlan(f"AutoAutomate::{need.name}", mode, self.oak_score(need, depth), drop, blockers, depth)

    def plans(self, needs: tuple[AutomationNeed, ...] | None = None, max_depth: int = 1) -> tuple[AutomationPlan, ...]:
        needs = needs or self.default_needs()
        items = [self.plan(n, d) for d in range(max_depth + 1) for n in needs]
        return tuple(sorted(items, key=lambda p: (p.oak_score, -len(p.blockers)), reverse=True))

    def work_order(self, plan: AutomationPlan) -> AutomationWorkOrder:
        approved = plan.mode == AutomationMode.DRY_RUN and not plan.blockers
        reason = "dry-run approved" if approved else "; ".join(plan.blockers) or "plan-only"
        return AutomationWorkOrder(plan.name, approved, reason, {
            "mode": plan.mode.value,
            "oak_score": plan.oak_score,
            "recursion_depth": plan.recursion_depth,
            "friction_drop": plan.friction_drop,
        })

    def run(self, max_depth: int = 1) -> tuple[tuple[AutomationPlan, ...], tuple[AutomationWorkOrder, ...]]:
        plans = self.plans(max_depth=max_depth)
        return plans, tuple(self.work_order(p) for p in plans)

    def markdown(self) -> str:
        plans, _orders = self.run()
        lines = ["# AIT AutoAutomation Kernel", "", "mode: meta_automation_guarded", ""]
        if plans:
            lines.append(f"best: `{plans[0].name}` OAK `{plans[0].oak_score}` mode `{plans[0].mode.value}`")
        lines.append("OAK invariant: automation need -> recursive plan -> anti-loop gate -> dry-run work order -> human handoff")
        return "\n".join(lines) + "\n"
