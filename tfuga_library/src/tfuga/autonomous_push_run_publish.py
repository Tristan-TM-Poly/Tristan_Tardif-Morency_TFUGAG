from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal

Phase = Literal["push", "run", "publish"]
Mode = Literal["dry_run", "review_required", "ready"]


@dataclass(frozen=True)
class PRPRequest:
    name: str
    phase: Phase
    target: str
    risk: str = "low"
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True)
class PRPPlan:
    request: PRPRequest
    mode: Mode
    oak_score: float
    route: str
    gates: tuple[str, ...]
    checklist: tuple[str, ...]


@dataclass(frozen=True)
class PRPReport:
    plans: tuple[PRPPlan, ...]
    ready: tuple[PRPPlan, ...]
    review: tuple[PRPPlan, ...]
    markdown: str


@dataclass(frozen=True)
class PRPPolicy:
    dry_run_default: bool = True
    min_oak_score: float = 7.0
    require_tests: bool = True
    require_docs: bool = True
    require_draft_pr: bool = True
    allow_external_publish: bool = False


class AITAutonomousPushRunPublish:
    """Dry-run-first OAK planner for push/run/publish workflows."""

    def __init__(self, policy: PRPPolicy | None = None) -> None:
        self.policy = policy or PRPPolicy()

    def plan(self, request: PRPRequest) -> PRPPlan:
        score = self._score(request)
        phase = request.phase
        if phase == "push":
            route = "branch -> commit -> draft PR -> review"
            gates = ("branch", "commit", "draft_pr", "review")
            checklist = ("confirm target branch", "attach commit", "open/update draft PR", "record OAK notes")
        elif phase == "run":
            route = "local checks -> test report -> OAK score"
            gates = ("tests", "static_check", "report")
            checklist = ("run deterministic tests", "capture output", "store report")
        else:
            route = "artifact -> release notes -> review gate"
            gates = ("artifact", "release_notes", "review")
            checklist = ("build artifact", "write release notes", "verify checksums", "wait for review")
            if self.policy.allow_external_publish:
                gates = gates + ("publish_gate",)
                checklist = checklist + ("publish only after explicit approval",)

        if self.policy.require_tests and "tests" not in gates:
            gates = gates + ("tests",)
        if self.policy.require_docs and "docs" not in gates:
            gates = gates + ("docs",)
        if self.policy.require_draft_pr and phase != "run" and "draft_pr" not in gates:
            gates = gates + ("draft_pr",)

        if self.policy.dry_run_default:
            mode: Mode = "dry_run"
        elif score >= self.policy.min_oak_score and request.risk != "high":
            mode = "ready"
        else:
            mode = "review_required"
        return PRPPlan(request, mode, score, route, tuple(gates), tuple(checklist))

    def generate(self, requests: Iterable[PRPRequest]) -> PRPReport:
        plans = tuple(self.plan(item) for item in requests)
        ready = tuple(item for item in plans if item.mode == "ready")
        review = tuple(item for item in plans if item.mode != "ready")
        return PRPReport(plans, ready, review, self.markdown(plans))

    def markdown(self, plans: Iterable[PRPPlan]) -> str:
        plans = tuple(plans)
        lines = ["# AIT Autonomous Push Run Publish Report", "", f"Plans: `{len(plans)}`", ""]
        for plan in plans:
            lines.append(f"## {plan.request.name}")
            lines.append(f"- phase: `{plan.request.phase}`")
            lines.append(f"- mode: `{plan.mode}`")
            lines.append(f"- OAK score: `{plan.oak_score}`")
            lines.append(f"- route: {plan.route}")
            lines.append(f"- gates: `{', '.join(plan.gates)}`")
            for item in plan.checklist:
                lines.append(f"- [ ] {item}")
            lines.append("")
        return "\n".join(lines).strip() + "\n"

    def default_requests(self) -> tuple[PRPRequest, ...]:
        return (
            PRPRequest("Push package branch", "push", "feature/tfuga-python-library", "low", ("commit", "draft_pr")),
            PRPRequest("Run package tests", "run", "tfuga_library", "low", ("pytest",)),
            PRPRequest("Publish artifact bundle", "publish", "sandbox artifact", "medium", ("zip", "manifest")),
        )

    def _score(self, request: PRPRequest) -> float:
        score = 5.0 + min(len(request.evidence), 3) * 1.0
        if request.risk == "low":
            score += 1.5
        elif request.risk == "medium":
            score += 0.5
        else:
            score -= 2.0
        if request.phase == "run":
            score += 0.5
        return round(max(0.0, min(10.0, score)), 2)
