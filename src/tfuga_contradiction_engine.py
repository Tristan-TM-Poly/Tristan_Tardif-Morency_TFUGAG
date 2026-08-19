"""Minimal local Contradiction Engine for TFUGAG.

This module detects simple textual contradiction candidates between Knowledge
Atoms. It does not prove logical inconsistency; it flags pairs that deserve
review before promotion.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import re

from src.tfuga_airgap import KnowledgeAtom


NEGATION_MARKERS = {
    "not", "never", "no", "cannot", "can't", "without",
    "pas", "jamais", "aucun", "aucune", "impossible", "sans",
}


@dataclass(frozen=True)
class ContradictionCandidate:
    left_id: str
    right_id: str
    score: float
    rationale: str

    def to_dict(self) -> dict:
        return asdict(self)


def normalize_claim(text: str) -> set[str]:
    tokens = re.findall(r"[A-Za-zÀ-ÿ0-9_\-]{3,}", text.lower())
    return {token for token in tokens if token not in NEGATION_MARKERS}


def has_negation(text: str) -> bool:
    tokens = set(re.findall(r"[A-Za-zÀ-ÿ0-9_\-]+", text.lower()))
    return bool(tokens & NEGATION_MARKERS)


def jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def contradiction_score(left: KnowledgeAtom, right: KnowledgeAtom) -> float:
    left_terms = normalize_claim(left.claim)
    right_terms = normalize_claim(right.claim)
    overlap = jaccard(left_terms, right_terms)
    negation_mismatch = has_negation(left.claim) != has_negation(right.claim)
    if not negation_mismatch:
        return 0.0
    return overlap


def propose_contradiction(left_id: str, left: KnowledgeAtom, right_id: str, right: KnowledgeAtom, threshold: float = 0.35) -> ContradictionCandidate | None:
    if left_id == right_id:
        return None
    score = contradiction_score(left, right)
    if score < threshold:
        return None
    rationale = f"Shared claim terms with opposite negation pattern; score={score:.3f}. Requires review."
    return ContradictionCandidate(left_id, right_id, round(score, 6), rationale)


def propose_contradictions(atoms: dict[str, KnowledgeAtom], threshold: float = 0.35) -> list[ContradictionCandidate]:
    ids = sorted(atoms)
    candidates: list[ContradictionCandidate] = []
    for index, left_id in enumerate(ids):
        for right_id in ids[index + 1 :]:
            candidate = propose_contradiction(left_id, atoms[left_id], right_id, atoms[right_id], threshold)
            if candidate is not None:
                candidates.append(candidate)
    return sorted(candidates, key=lambda item: item.score, reverse=True)
