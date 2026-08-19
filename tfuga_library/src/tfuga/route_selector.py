from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class RouteGoal:
    name: str
    category: str
    target: str
    priority: int = 5


@dataclass(frozen=True)
class RoutePlan:
    goal: RouteGoal
    oak_score: float
    route: str
    gates: tuple[str, ...]
    note: str


class AITRouteSelector:
    """Selects OAK routes for TFUGA work items."""

    def plan(self, goal: RouteGoal) -> RoutePlan:
        category = goal.category.lower().strip()
        if category == "repo":
            return RoutePlan(goal, 8.5, "branch -> draft PR -> tests -> docs -> review", ("branch", "draft_pr", "tests", "docs", "review"), "repository-native activation")
        if category == "adapter":
            return RoutePlan(goal, 8.0, "capability card -> adapter -> tests -> docs", ("capability_card", "adapter", "tests", "docs"), "capability integration path")
        if category == "review":
            return RoutePlan(goal, 5.0, "proposal -> review -> next decision", ("proposal", "review"), "review queue path")
        return RoutePlan(goal, 7.0, "artifact -> tests -> docs -> proposal", ("artifact", "tests", "docs", "proposal"), "local artifact path")

    def plan_many(self, goals: Iterable[RouteGoal]) -> tuple[RoutePlan, ...]:
        return tuple(self.plan(goal) for goal in goals)

    def markdown(self, plans: Iterable[RoutePlan]) -> str:
        plans = tuple(plans)
        lines = ["# AIT Route Selector Report", "", f"Plans: `{len(plans)}`", ""]
        for plan in plans:
            lines.append(f"## {plan.goal.name}")
            lines.append(f"- score: `{plan.oak_score}`")
            lines.append(f"- route: {plan.route}")
            lines.append(f"- gates: `{', '.join(plan.gates)}`")
            lines.append(f"- note: {plan.note}")
            lines.append("")
        return "\n".join(lines).strip() + "\n"

    def default_goals(self) -> tuple[RouteGoal, ...]:
        return (
            RouteGoal("Repository package update", "repo", "github", 9),
            RouteGoal("External capability integration", "adapter", "api", 8),
            RouteGoal("Local module artifact", "artifact", "workspace", 7),
            RouteGoal("Review queue item", "review", "planning", 5),
        )
