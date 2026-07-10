"""Local text-to-Knowledge-Atom helpers for TFUGAG.

This module uses simple deterministic heuristics. It is meant to prepare
review packets, not to replace reading, proof, citation, or human judgment.
"""

from __future__ import annotations

import re
from collections import Counter

from src.tfuga_airgap import DCTStatus, KnowledgeAtom


STOPWORDS = {
    "the", "and", "or", "of", "to", "in", "a", "an", "for", "with", "on", "by",
    "le", "la", "les", "de", "des", "du", "et", "ou", "un", "une", "pour", "dans",
    "que", "qui", "sur", "avec", "est", "sont", "this", "that", "is", "are",
}


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def split_sentences(text: str) -> list[str]:
    cleaned = normalize_text(text)
    if not cleaned:
        return []
    parts = re.split(r"(?<=[.!?])\s+", cleaned)
    return [part.strip() for part in parts if part.strip()]


def extract_keywords(text: str, limit: int = 8) -> list[str]:
    tokens = re.findall(r"[A-Za-zÀ-ÿ0-9_\-]{3,}", text.lower())
    tokens = [token for token in tokens if token not in STOPWORDS]
    counts = Counter(tokens)
    return [word for word, _ in counts.most_common(limit)]


def infer_status(text: str) -> DCTStatus:
    lowered = text.lower()
    evidence_markers = ["test", "preuve", "proof", "simulation", "benchmark", "calculation", "calcul"]
    definition_markers = ["definition", "définition", "assumption", "hypothèse", "limitation", "model", "modèle"]
    if any(marker in lowered for marker in evidence_markers):
        return DCTStatus.DEMONSTRATED
    if any(marker in lowered for marker in definition_markers):
        return DCTStatus.CRYSTALLIZABLE
    if len(split_sentences(text)) >= 3:
        return DCTStatus.EXPLORATORY
    return DCTStatus.SPECULATIVE


def make_atom_from_text(title: str, text: str) -> KnowledgeAtom:
    sentences = split_sentences(text)
    claim = sentences[0] if sentences else "No claim supplied."
    keywords = extract_keywords(text)
    assumptions = [f"Key term present: {kw}" for kw in keywords[:3]] or ["Needs explicit assumptions."]
    evidence = [sentence for sentence in sentences if any(word in sentence.lower() for word in ["test", "proof", "preuve", "simulation", "benchmark", "calcul"])]
    limitations = ["Automatically extracted draft; requires review."]
    next_action = "Review the atom, reduce overclaims, and add evidence or downgrade status."
    return KnowledgeAtom(
        title=title,
        claim=claim,
        status=infer_status(text),
        assumptions=assumptions,
        evidence=evidence,
        limitations=limitations,
        next_action=next_action,
    )
