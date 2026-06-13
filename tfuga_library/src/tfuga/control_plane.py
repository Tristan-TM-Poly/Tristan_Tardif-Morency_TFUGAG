from __future__ import annotations

from dataclasses import dataclass

from .autonomous_push_run_publish import AITAutonomousPushRunPublish, PRPRequest
from .delivery_harness import DeliveryHarnessAdapter, DeliverySignal
from .quebec_research_absorber import AITQuebecResearchAbsorber
from .route_selector import AITRouteSelector, RouteGoal


@dataclass(frozen=True)
class ControlPlaneInput:
    name: str
    changed_files: int
    additions: int
    tests_added: int
    docs_added: int
    include_quebec_research: bool = True


@dataclass(frozen=True)
class ControlPlaneReport:
    name: str
    oak_score: float
    delivery_risk: str
    route_markdown: str
    push_run_publish_markdown: str
    research_markdown: str
    final_markdown: str


class AITControlPlane:
    """Central TFUGA/OAK planner producing a single reviewable report."""

    def run(self, item: ControlPlaneInput) -> ControlPlaneReport:
        delivery = DeliveryHarnessAdapter().assess(
            DeliverySignal(
                changed_files=item.changed_files,
                additions=item.additions,
                tests_added=item.tests_added,
                docs_added=item.docs_added,
            )
        )

        selector = AITRouteSelector()
        route_goals = (
            RouteGoal("Repository package update", "repo", "github", 9),
            RouteGoal("Artifact publication plan", "artifact", "workspace", 7),
            RouteGoal("Review queue", "review", "planning", 5),
        )
        route_markdown = selector.markdown(selector.plan_many(route_goals))

        prp = AITAutonomousPushRunPublish()
        prp_report = prp.generate((
            PRPRequest("Push branch update", "push", "feature/tfuga-python-library", "low", ("commit", "draft_pr")),
            PRPRequest("Run validation", "run", "tfuga_library", "low", ("tests", "report")),
            PRPRequest("Publish artifact note", "publish", "sandbox", "medium", ("zip", "manifest")),
        ))

        research_markdown = ""
        if item.include_quebec_research:
            research = AITQuebecResearchAbsorber()
            research_markdown = research.markdown_report(research.default_cards())

        oak_score = round((delivery.oak_score + 8.5 + 8.0) / 3.0, 2)
        final = self._render(item, delivery.risk, delivery.oak_score, oak_score, route_markdown, prp_report.markdown, research_markdown)

        return ControlPlaneReport(
            name=item.name,
            oak_score=oak_score,
            delivery_risk=delivery.risk,
            route_markdown=route_markdown,
            push_run_publish_markdown=prp_report.markdown,
            research_markdown=research_markdown,
            final_markdown=final,
        )

    def _render(self, item: ControlPlaneInput, risk: str, delivery_score: float, oak_score: float, route_markdown: str, prp_markdown: str, research_markdown: str) -> str:
        lines = [
            "# AIT Control Plane Max Report",
            "",
            f"Item: `{item.name}`",
            f"OAK score: `{oak_score}`",
            f"Delivery risk: `{risk}`",
            f"Delivery score: `{delivery_score}`",
            "",
            "## Route layer",
            "",
            route_markdown.strip(),
            "",
            "## Push / run / publish layer",
            "",
            prp_markdown.strip(),
        ]
        if research_markdown:
            lines.extend(["", "## Quebec research absorption layer", "", research_markdown.strip()])
        lines.extend(["", "## Final invariant", "", "analysis -> route -> gates -> local validation -> artifact -> draft PR"])
        return "\n".join(lines).strip() + "\n"
