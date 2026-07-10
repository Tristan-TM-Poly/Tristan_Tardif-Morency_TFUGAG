from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class RunResult:
    name: str
    passed: bool
    output: Any = None
    error: str | None = None


class Runner:
    def run(self, name: str, fn: Callable[[], Any]) -> RunResult:
        try:
            return RunResult(name, True, fn(), None)
        except Exception as error:
            return RunResult(name, False, None, str(error))
