from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JKDZeroTouchPact:
    mode: str = "zero_touch_oak_guarded"
    invariant: str = "idea -> formalization -> module -> tests -> OAK -> artifact -> GitHub -> safe handoff"

    def command(self) -> str:
        return (
            "JKD-ZERO-TOUCH POUR TOI ET MOI : Tristan = Architecte/Noeud Zero, "
            "ChatGPT = Operateur/Meta-Cortex. Cree, formalise, teste, zip, pousse GitHub, "
            "verifie PR, et garde tout live/officiel/irreversible en dry-run OAK."
        )

    def rules(self) -> tuple[str, ...]:
        return (
            "assume reasonable defaults",
            "create artifacts directly",
            "test when possible",
            "push to GitHub when possible",
            "verify final PR status",
            "keep live or official actions in dry-run or human handoff",
        )
