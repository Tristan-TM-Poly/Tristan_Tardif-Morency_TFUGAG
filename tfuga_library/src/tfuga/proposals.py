from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import PurePosixPath

_ALLOWED_PREFIXES = ("src/", "tests/", "docs/", "generated/", "proposals/", "examples/", "pyproject.toml", "README.md")
_FORBIDDEN_PREFIXES = (".git/", ".github/workflows/")
_RESTRICTED_MARKERS = ("raw dynamic execution marker", "shell destructive marker", "credential material marker")


@dataclass(frozen=True)
class ProposalChange:
    path: str
    content: str
    mode: str = "create_or_update"

    def normalized_path(self) -> str:
        path = str(PurePosixPath(self.path))
        if path.startswith("../") or path.startswith("/") or path == "..":
            raise ValueError(f"unsafe path: {self.path}")
        return path


@dataclass(frozen=True)
class Proposal:
    id: str
    title: str
    oak_score: float
    changes: list[ProposalChange]
    memory_negative: list[str] = field(default_factory=list)
    memory_positive: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ProposalValidation:
    passed: bool
    errors: list[str]
    warnings: list[str]


class ProposalValidator:
    def __init__(self, min_oak_score: float = 5.0) -> None:
        self.min_oak_score = min_oak_score

    def validate(self, proposal: Proposal) -> ProposalValidation:
        errors: list[str] = []
        warnings: list[str] = []
        if proposal.oak_score < self.min_oak_score:
            errors.append("oak score below threshold")
        if not proposal.changes:
            errors.append("proposal has no changes")
        for change in proposal.changes:
            try:
                path = change.normalized_path()
            except ValueError as exc:
                errors.append(str(exc))
                continue
            if any(path.startswith(prefix) for prefix in _FORBIDDEN_PREFIXES):
                errors.append(f"forbidden target path: {path}")
            if not any(path.startswith(prefix) or path == prefix for prefix in _ALLOWED_PREFIXES):
                errors.append(f"target path not whitelisted: {path}")
            lowered = change.content.lower()
            for marker in _RESTRICTED_MARKERS:
                if marker in lowered:
                    errors.append(f"restricted marker in {path}: {marker}")
            if len(change.content) > 1_000_000:
                warnings.append(f"large proposal file: {path}")
        return ProposalValidation(passed=not errors, errors=errors, warnings=warnings)
