from __future__ import annotations

import re

from .cvcd import CVCDScorer
from .hgfm import HGFMMapper
from .oak import OAKValidator
from .specs import AITPacket, AITSpec


def _slug_title(goal: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", goal.title())
    return "".join(words[:6]) or "GeneratedAIT"


class AITGenerator:
    """Generate OAK-validated AIT packets from goals."""

    def __init__(
        self,
        hgfm: HGFMMapper | None = None,
        cvcd: CVCDScorer | None = None,
        oak: OAKValidator | None = None,
    ) -> None:
        self.hgfm = hgfm or HGFMMapper()
        self.cvcd = cvcd or CVCDScorer()
        self.oak = oak or OAKValidator()

    def compile_goal(self, goal: str) -> AITSpec:
        clean_goal = goal.strip() or "Generate a testable AIT"
        title = _slug_title(clean_goal)
        return AITSpec(
            name=f"AIT-{title}",
            mission=f"Transform the goal into validated traces, prototypes, tests, and residues: {clean_goal}",
            inputs=["goal", "constraints", "memory_context", "examples"],
            outputs=["AITSpec", "HGFM_map", "OAK_report", "prototype_plan", "residue_log"],
            tools=["reasoning", "decomposition", "code_generation", "benchmark_design"],
            validators=["coherence_check", "counterexample_search", "prototype_smoke_test"],
            memory_read=["Alexandrie/core", "Alexandrie/residues"],
            memory_write=["Alexandrie/ait2/generated", "Alexandrie/ait2/residues"],
            yield_targets=["knowledge", "prototype", "publication_seed", "recognition"],
            oak_min_status=2,
            assumptions=[
                "Generated AITs are scaffolds, not autonomous proof of correctness.",
                "Strong claims must be promoted only through tests, proofs, or counterexample resistance.",
            ],
        )

    def generate(self, goal: str) -> AITPacket:
        spec = self.compile_goal(goal)
        graph = self.hgfm.map(spec)
        score = self.cvcd.score(graph)
        report = self.oak.validate(spec, graph, score)
        residues = list(graph.get("residues", [])) + report.residues
        return AITPacket(
            spec=spec,
            hgfm=graph,
            cvcd_score=score,
            oak_report=report,
            residues=sorted(set(residues)),
        )
