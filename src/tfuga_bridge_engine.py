"""Local deterministic Bridge Engine for TFUGAG.

This module proposes candidate relations between Knowledge Atoms using token
similarity. It is intentionally simple: candidate bridges must still be reviewed
before entering the canon.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import math
import re
from collections import Counter

from src.tfuga_airgap import KnowledgeAtom
from src.tfuga_graph import RelationType


@dataclass(frozen=True)
class BridgeCandidate:
    source_id: str
    target_id: str
    relation: RelationType
    score: float
    rationale: str

    def to_dict(self) -> dict:
        return asdict(self)


def tokenize(text: str) -> list[str]:
    return re.findall(r"[A-Za-zÀ-ÿ0-9_\-]{3,}", text.lower())


def atom_text(atom: KnowledgeAtom) -> str:
    return " ".join(
        [
            atom.title,
            atom.claim,
            " ".join(atom.assumptions),
            " ".join(atom.evidence),
            " ".join(atom.limitations),
            atom.next_action,
        ]
    )


def term_vector(text: str) -> Counter:
    return Counter(tokenize(text))


def cosine_similarity(left: Counter, right: Counter) -> float:
    if not left or not right:
        return 0.0
    keys = set(left) | set(right)
    dot = sum(left[key] * right[key] for key in keys)
    norm_left = math.sqrt(sum(value * value for value in left.values()))
    norm_right = math.sqrt(sum(value * value for value in right.values()))
    if norm_left == 0 or norm_right == 0:
        return 0.0
    return dot / (norm_left * norm_right)


def propose_bridge(source_id: str, source: KnowledgeAtom, target_id: str, target: KnowledgeAtom, threshold: float = 0.25) -> BridgeCandidate | None:
    if source_id == target_id:
        return None
    score = cosine_similarity(term_vector(atom_text(source)), term_vector(atom_text(target)))
    if score < threshold:
        return None
    relation = RelationType.ANALOGOUS_TO
    rationale = f"Token-space similarity {score:.3f} suggests a candidate analogy requiring review."
    return BridgeCandidate(source_id, target_id, relation, round(score, 6), rationale)


def propose_bridges(atoms: dict[str, KnowledgeAtom], threshold: float = 0.25) -> list[BridgeCandidate]:
    ids = sorted(atoms)
    candidates: list[BridgeCandidate] = []
    for index, source_id in enumerate(ids):
        for target_id in ids[index + 1 :]:
            candidate = propose_bridge(source_id, atoms[source_id], target_id, atoms[target_id], threshold)
            if candidate is not None:
                candidates.append(candidate)
    return sorted(candidates, key=lambda item: item.score, reverse=True)
