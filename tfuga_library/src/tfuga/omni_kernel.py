from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from enum import Enum


class KernelMode(str, Enum):
    DRY_RUN = "dry_run"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class IgniteConfig:
    topology: str = "sedenionic-16D"
    action_engine: str = "mycelial"
    orchestrator: str = "auto-automation"
    policy: str = "ZERO-TOUCH"
    handoff_threshold: float | None = None
    oak_strict_mode: bool = True
    environment: str = "production"


@dataclass(frozen=True)
class KernelGate:
    name: str
    passed: bool
    severity: str
    reason: str


@dataclass(frozen=True)
class IgniteReport:
    mode: KernelMode
    config: IgniteConfig
    gates: tuple[KernelGate, ...]
    global_action: float
    next_action: str
    markdown: str


class TFUGAOmniKernel:
    allowed_topologies = {"sedenionic-16D", "vector-16D", "scalar-demo"}
    allowed_action_engines = {"mycelial", "least-action", "review-only"}
    allowed_orchestrators = {"auto-automation", "review-packet", "none"}
    allowed_policies = {"ZERO-TOUCH", "OAK-STRICT", "REVIEW-ONLY"}

    def validate(self, config: IgniteConfig) -> tuple[KernelGate, ...]:
        gates = [
            KernelGate("topology", config.topology in self.allowed_topologies, "error", "supported" if config.topology in self.allowed_topologies else "unsupported"),
            KernelGate("action_engine", config.action_engine in self.allowed_action_engines, "error", "supported" if config.action_engine in self.allowed_action_engines else "unsupported"),
            KernelGate("orchestrator", config.orchestrator in self.allowed_orchestrators, "error", "supported" if config.orchestrator in self.allowed_orchestrators else "unsupported"),
            KernelGate("policy", config.policy in self.allowed_policies, "error", "supported" if config.policy in self.allowed_policies else "unsupported"),
            KernelGate("handoff_override", config.handoff_threshold is None, "critical", "not requested" if config.handoff_threshold is None else "override blocked; approval gates remain active"),
            KernelGate("oak_strict", config.oak_strict_mode, "critical", "active" if config.oak_strict_mode else "must remain active"),
        ]
        return tuple(gates)

    def ignite(self, config: IgniteConfig) -> IgniteReport:
        gates = self.validate(config)
        blocked = any((not g.passed and g.severity in {"critical", "error"}) for g in gates)
        mode = KernelMode.BLOCKED if blocked else KernelMode.DRY_RUN
        base = 35.0
        penalty = sum(3.0 if not g.passed and g.severity == "critical" else 1.0 if not g.passed else 0.0 for g in gates)
        action = round(base - penalty, 4)
        next_action = "resolve OAK blockers" if blocked else "emit dry-run work orders and review packet"
        report = IgniteReport(mode, config, gates, action, next_action, "")
        return IgniteReport(mode, config, gates, action, next_action, self.markdown(report))

    def markdown(self, report: IgniteReport) -> str:
        lines = ["# TFUGA Omni Kernel Ignite", "", f"mode: `{report.mode.value}`", ""]
        lines.append(f"global_action_tensor: `{report.global_action}`")
        lines.append(f"next_action: {report.next_action}")
        lines.append("\n## OAK gates")
        for gate in report.gates:
            mark = "x" if gate.passed else " "
            lines.append(f"- [{mark}] `{gate.name}` severity `{gate.severity}` :: {gate.reason}")
        lines.append("\nInvariant: topology + action_engine + orchestrator + policy -> OAK gates -> dry-run/report -> authorized handoff")
        return "\n".join(lines) + "\n"

    def to_json(self, report: IgniteReport) -> str:
        return json.dumps({
            "mode": report.mode.value,
            "config": asdict(report.config),
            "gates": [asdict(g) for g in report.gates],
            "global_action": report.global_action,
            "next_action": report.next_action,
        }, indent=2)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m tfuga.omni_kernel")
    sub = parser.add_subparsers(dest="command", required=True)
    ignite = sub.add_parser("ignite")
    ignite.add_argument("--topology", default="sedenionic-16D")
    ignite.add_argument("--action-engine", default="mycelial")
    ignite.add_argument("--orchestrator", default="auto-automation")
    ignite.add_argument("--policy", default="ZERO-TOUCH")
    ignite.add_argument("--handoff-threshold", type=float, default=None)
    ignite.add_argument("--env", default="production")
    ignite.add_argument("--oak-strict-mode", type=int, default=1)
    ignite.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = IgniteConfig(args.topology, args.action_engine, args.orchestrator, args.policy, args.handoff_threshold, bool(args.oak_strict_mode), args.env)
    kernel = TFUGAOmniKernel()
    report = kernel.ignite(config)
    print(kernel.to_json(report) if args.json else report.markdown)
    return 2 if report.mode == KernelMode.BLOCKED else 0


if __name__ == "__main__":
    raise SystemExit(main())
