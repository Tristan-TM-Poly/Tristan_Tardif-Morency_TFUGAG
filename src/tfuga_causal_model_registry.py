"""TFUGAG Causal Model Registry.

Descriptive registry for causal hypotheses. It separates correlation from
causal claims and records assumptions, mechanisms, observations, and possible
counterexamples. It does not run studies or assert proof.
"""
from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

class CausalLinkType(str, Enum):
    HYPOTHETICAL_CAUSE = "hypothetical_cause"
    HYPOTHETICAL_INHIBITOR = "hypothetical_inhibitor"
    ENABLES = "enables"
    CORRELATION_ONLY = "correlation_only"
    POSSIBLE_CONFOUNDER = "possible_confounder"
    POSSIBLE_COUNTEREXAMPLE = "possible_counterexample"

@dataclass(frozen=True)
class CausalVariable:
    variable_id: str
    name: str
    description: str
    domain: str

@dataclass(frozen=True)
class CausalHypothesis:
    hypothesis_id: str
    source_variable_id: str
    target_variable_id: str
    link_type: CausalLinkType
    proposed_mechanism: str
    assumptions: list[str]
    observation_refs: list[str]
    limitations: list[str]

@dataclass
class CausalModelRegistry:
    variables: dict
    hypotheses: dict

    @classmethod
    def empty(cls):
        return cls({}, {})

    def add_variable(self, node: CausalVariable):
        self.variables[node.variable_id] = node

    def add_hypothesis(self, hypothesis: CausalHypothesis):
        self.hypotheses[hypothesis.hypothesis_id] = hypothesis

    def to_dict(self):
        return {
            "schema": "tfugag.causal_model_registry.v1",
            "variables": [asdict(v) for v in self.variables.values()],
            "hypotheses": [asdict(h) for h in self.hypotheses.values()],
        }


def write_causal_registry(registry: CausalModelRegistry, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    return path
