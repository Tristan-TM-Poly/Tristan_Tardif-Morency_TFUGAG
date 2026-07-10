from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReviewGate:
    name: str
    passed: bool
    weight: float
    evidence: str


@dataclass(frozen=True)
class ReviewPacket:
    score: float
    ready: bool
    blockers: tuple[str, ...]
    next_action: str


class TFUGAReviewPacket:
    def gates(self) -> tuple[ReviewGate, ...]:
        return (
            ReviewGate("artifact created", True, 1.0, "zip exists"),
            ReviewGate("local checks", True, 1.0, "green locally"),
            ReviewGate("pull request exists", True, 1.0, "verified"),
            ReviewGate("pull request can be integrated", True, 1.0, "reported true"),
            ReviewGate("draft flag cleared", False, 1.0, "still draft"),
            ReviewGate("external proof attached", False, 1.0, "not attached"),
        )

    def score(self, gates: tuple[ReviewGate, ...]) -> float:
        total = sum(g.weight for g in gates)
        passed = sum(g.weight for g in gates if g.passed)
        return round(10.0 * passed / total, 4) if total else 0.0

    def packet(self, gates: tuple[ReviewGate, ...] | None = None) -> ReviewPacket:
        gates = gates or self.gates()
        score = self.score(gates)
        blockers = tuple(f"{g.name}: {g.evidence}" for g in gates if not g.passed)
        ready = score >= 9.0 and not blockers
        action = "ready" if ready else "resolve blockers"
        return ReviewPacket(score, ready, blockers, action)

    def markdown(self) -> str:
        packet = self.packet()
        lines = ["# TFUGA Review Packet", "", "mode: decision_packet", ""]
        lines.append(f"- score: `{packet.score}`")
        lines.append(f"- ready: `{packet.ready}`")
        lines.append(f"- next_action: {packet.next_action}")
        return "\n".join(lines).strip() + "\n"
