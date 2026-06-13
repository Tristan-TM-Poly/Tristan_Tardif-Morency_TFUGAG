from __future__ import annotations

from typing import Any

from .specs import AITSpec, OAKReport


class OAKValidator:
    """Operational Analysis Kernel gate for generated AITs."""

    def validate(self, spec: AITSpec, hgfm: dict[str, Any], cvcd_score: float) -> OAKReport:
        strengths: list[str] = []
        weaknesses: list[str] = []
        residues: list[str] = list(hgfm.get("residues", []))
        tests: list[str] = []
        next_actions: list[str] = []

        if spec.mission and spec.inputs and spec.outputs:
            strengths.append("Mission, inputs, and outputs are explicit.")
        else:
            weaknesses.append("Mission, inputs, or outputs are underspecified.")

        if spec.validators:
            strengths.append("Validators are declared.")
            tests.extend([f"Run validator: {validator}" for validator in spec.validators])
        else:
            weaknesses.append("No validators declared.")

        if spec.memory_write:
            strengths.append("Memory write targets preserve traces and residues.")
        else:
            weaknesses.append("No memory write target declared.")

        if cvcd_score >= 0.70:
            status = 4
        elif cvcd_score >= 0.55:
            status = 3
        elif cvcd_score >= 0.35 and tests:
            status = 2
        elif cvcd_score >= 0.20:
            status = 1
        else:
            status = 0

        if status < spec.oak_min_status:
            residues.append(
                f"OAK status {status} is below required threshold {spec.oak_min_status}."
            )
            next_actions.append("Add validators, examples, tests, or narrower outputs.")
        else:
            next_actions.append("Generate executable prototype and benchmark packet.")

        if not tests:
            next_actions.append("Create at least one falsifiable test before promotion.")

        return OAKReport(
            status=status,
            strengths=strengths,
            weaknesses=weaknesses,
            residues=residues,
            tests=tests,
            next_actions=next_actions,
        )
