from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class FileSignal:
    path: str
    lines: int
    classes: int
    functions: int
    imports: int
    todos: int
    docstring: bool
    oak_score: float
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class RepoSignal:
    files: tuple[FileSignal, ...]
    oak_score: float
    top_actions: tuple[str, ...]


class AITCodeAnalyserWriter:
    """Analyze code snapshots and write OAK-oriented improvement reports."""

    def analyse_python(self, path: str, source: str) -> FileSignal:
        lines = [line for line in source.splitlines() if line.strip()]
        todos = sum(1 for line in source.splitlines() if "TODO" in line or "FIXME" in line)
        notes: list[str] = []
        try:
            tree = ast.parse(source)
        except SyntaxError as error:
            return FileSignal(path, len(lines), 0, 0, 0, todos, False, 1.0, (f"syntax issue: {error.msg}",))

        classes = sum(isinstance(node, ast.ClassDef) for node in ast.walk(tree))
        functions = sum(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) for node in ast.walk(tree))
        imports = sum(isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(tree))
        docstring = ast.get_docstring(tree) is not None

        score = 5.0
        if docstring:
            score += 1.0
        else:
            notes.append("add module docstring")
        if functions or classes:
            score += 1.0
        if todos:
            score -= min(2.0, todos * 0.5)
            notes.append("convert TODO/FIXME markers into tracked proposals")
        if len(lines) > 300:
            score -= 1.0
            notes.append("split large module or add section documentation")
        if imports == 0 and functions + classes > 2:
            notes.append("check whether shared helpers should be extracted")
        score = max(0.0, min(10.0, score))
        return FileSignal(path, len(lines), classes, functions, imports, todos, docstring, score, tuple(notes))

    def analyse_many(self, files: Iterable[tuple[str, str]]) -> RepoSignal:
        signals = tuple(self.analyse_python(path, source) for path, source in files if path.endswith(".py"))
        if not signals:
            return RepoSignal((), 0.0, ("add Python files to analyze",))
        score = round(sum(item.oak_score for item in signals) / len(signals), 2)
        actions: list[str] = []
        weak = sorted(signals, key=lambda item: item.oak_score)[:5]
        for item in weak:
            for note in item.notes:
                actions.append(f"{item.path}: {note}")
        if not actions:
            actions.append("repository layer is locally coherent; add examples and CI next")
        return RepoSignal(signals, score, tuple(actions[:10]))

    def markdown_report(self, signal: RepoSignal, title: str = "AIT Code Analysis") -> str:
        lines = [f"# {title}", "", f"OAK repository score: `{signal.oak_score}`", "", "## Files", ""]
        for item in signal.files:
            lines.append(f"- `{item.path}` — score `{item.oak_score}`, lines `{item.lines}`, functions `{item.functions}`, classes `{item.classes}`")
        lines.extend(["", "## Top actions", ""])
        for action in signal.top_actions:
            lines.append(f"- {action}")
        return "\n".join(lines).strip() + "\n"

    def proposal_markdown(self, signal: RepoSignal) -> str:
        lines = ["# AIT Improvement Proposal", "", "## Proposed actions", ""]
        for action in signal.top_actions:
            lines.append(f"- [ ] {action}")
        lines.extend(["", "## Activation", "", "Use branch, draft PR, tests, and OAK-positive review."])
        return "\n".join(lines).strip() + "\n"
