from __future__ import annotations

from typing import Any

from .specs import AITSpec


class HGFMMapper:
    """Build a lightweight HyperGraph Fractal Mycelial map from an AIT spec."""

    def map(self, spec: AITSpec) -> dict[str, Any]:
        nodes: list[dict[str, str]] = [{"id": spec.name, "kind": "ait", "label": spec.mission}]
        hyperedges: list[dict[str, Any]] = []

        def add_many(kind: str, values: list[str]) -> None:
            for index, value in enumerate(values):
                node_id = f"{kind}:{index}:{value}"
                nodes.append({"id": node_id, "kind": kind, "label": value})
                hyperedges.append({"source": spec.name, "targets": [node_id], "relation": f"has_{kind}"})

        add_many("input", spec.inputs)
        add_many("output", spec.outputs)
        add_many("tool", spec.tools)
        add_many("validator", spec.validators)
        add_many("yield", spec.yield_targets)

        residues = []
        if not spec.validators:
            residues.append("No validators supplied; OAK cannot promote the AIT.")
        if not spec.outputs:
            residues.append("No outputs supplied; generated AIT is not observable.")
        if spec.oak_min_status < 2:
            residues.append("OAK threshold is below testable maturity.")

        return {
            "root": spec.name,
            "nodes": nodes,
            "hyperedges": hyperedges,
            "memory": {"read": spec.memory_read, "write": spec.memory_write},
            "residues": residues,
        }
