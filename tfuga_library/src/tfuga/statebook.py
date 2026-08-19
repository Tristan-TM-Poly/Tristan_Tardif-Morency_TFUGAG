from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StateStep:
    name: str
    state: str
    note: str


class StateBook:
    def sequence(self, token: str) -> list[StateStep]:
        return [
            StateStep("verify", "ready", token),
            StateStep("branch", "ready", "visible branch exists"),
            StateStep("draft", "ready", "pull request exists"),
            StateStep("review", "pending", "keep OAK gate visible"),
        ]
