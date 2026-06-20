from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class AgentAction:
    name: str
    purpose: str
    risk: str = "low"


@dataclass(frozen=True)
class AgentTrace:
    accepted: tuple[AgentAction, ...]
    rejected: tuple[AgentAction, ...]
    notes: tuple[str, ...]


@dataclass
class AgentHarnessAdapter:
    """Mediates proposed actions through simple OAK-style constraints."""

    allowed_actions: set[str] = field(default_factory=lambda: {"read", "analyze", "write_artifact", "open_pr", "update_pr"})
    max_high_risk: int = 0

    def filter_actions(self, actions: list[AgentAction]) -> AgentTrace:
        accepted: list[AgentAction] = []
        rejected: list[AgentAction] = []
        notes: list[str] = []
        high_risk_count = 0
        for action in actions:
            if action.name not in self.allowed_actions:
                rejected.append(action)
                notes.append(f"rejected unknown action: {action.name}")
                continue
            if action.risk == "high":
                high_risk_count += 1
                if high_risk_count > self.max_high_risk:
                    rejected.append(action)
                    notes.append(f"rejected high risk action: {action.name}")
                    continue
            accepted.append(action)
        if not notes:
            notes.append("all actions accepted")
        return AgentTrace(tuple(accepted), tuple(rejected), tuple(notes))
