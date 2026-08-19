from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class StatusModule:
    name: str
    role: str
    maturity: int
    tests: int
    docs: bool


@dataclass(frozen=True)
class StatusReport:
    score: float
    markdown: str


class AITStatusBoard:
    def default_modules(self) -> tuple[StatusModule, ...]:
        return (
            StatusModule("AITCodeAnalyserWriter", "code reports", 7, 3, True),
            StatusModule("AITCapabilityAbsorber", "capability cards", 7, 3, True),
            StatusModule("DeliveryHarnessAdapter", "delivery gates", 7, 1, True),
            StatusModule("AITAutonomousGenesis", "proposal generation", 7, 4, True),
            StatusModule("AITRouteSelector", "route planning", 7, 4, True),
            StatusModule("AITQuebecResearchAbsorber", "research mapping", 7, 4, True),
            StatusModule("AITAutonomousPushRunPublish", "workflow planning", 8, 5, True),
            StatusModule("AITControlPlane", "central report", 8, 2, True),
        )

    def score(self, modules: Iterable[StatusModule]) -> float:
        modules = tuple(modules)
        if not modules:
            return 0.0
        total = 0.0
        for module in modules:
            item = module.maturity + min(module.tests, 5) * 0.35 + (0.75 if module.docs else 0.0)
            total += min(item, 10.0)
        return round(total / len(modules), 2)

    def report(self, modules: Iterable[StatusModule] | None = None) -> StatusReport:
        modules = tuple(modules or self.default_modules())
        score = self.score(modules)
        lines = ["# AIT Status Board", "", f"Score: `{score}`", "", "## Modules", ""]
        for module in modules:
            lines.append(f"- `{module.name}` — {module.role}; maturity `{module.maturity}`; tests `{module.tests}`; docs `{module.docs}`")
        lines.extend(["", "## Next", "", "- [ ] Add integration tests", "- [ ] Add generated PR report", "- [ ] Add examples for low-test modules"])
        return StatusReport(score, "\n".join(lines).strip() + "\n")
