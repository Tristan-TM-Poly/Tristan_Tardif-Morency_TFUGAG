from __future__ import annotations

from dataclasses import asdict, dataclass
import json


@dataclass(frozen=True)
class GitHubActivationPlan:
    repository: str
    base_branch: str
    branch_name: str
    commit_sha: str
    title: str
    body: str

    def ref_payload(self) -> dict:
        return {"ref": f"refs/heads/{self.branch_name}", "sha": self.commit_sha}

    def pr_payload(self) -> dict:
        return {"title": self.title, "head": self.branch_name, "base": self.base_branch, "body": self.body, "draft": True}

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, ensure_ascii=False)


class GitHubOrchestrator:
    """Creates branch/PR planning payloads for trusted repository tools."""

    def build_plan(self, repository: str, commit_sha: str, branch_name: str = "feature/tfuga-python-library", base_branch: str = "main") -> GitHubActivationPlan:
        body = (
            "Adds TFUGA Python library for CVCD, HGFM, OAK, proposals, memory, "
            "and repository orchestration planning.\n\n"
            "Activation invariant: branch -> draft PR -> CI -> OAK-positive merge."
        )
        return GitHubActivationPlan(repository, base_branch, branch_name, commit_sha, "[codex] Add TFUGA Python library", body)

    def issue_body(self, plan: GitHubActivationPlan, tests_summary: str) -> str:
        return (
            "# TFUGA Python library ready\n\n"
            f"Repository: `{plan.repository}`\n\n"
            f"Commit: `{plan.commit_sha}`\n\n"
            f"Branch target: `{plan.branch_name}`\n\n"
            f"Validation: `{tests_summary}`\n\n"
            "This issue records the library as a zero-touch activation artifact.\n"
        )
