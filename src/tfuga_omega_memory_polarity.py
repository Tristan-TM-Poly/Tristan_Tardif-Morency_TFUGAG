"""TFUGAG Omega Memory Polarity.

Stores positive and negative learning records for TFUGAG. Negative memory records
failures, limits, blocked paths, contradictions and rejected proposals. Positive
memory records validated capabilities, successful patterns, promoted claims and
reusable strategies.

This module is descriptive and review-oriented. It does not execute actions,
call external systems, self-modify, or mutate canon.
"""
from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

class MemoryPolarity(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"

class MemoryRecordKind(str, Enum):
    FAILURE = "failure"
    LIMIT = "limit"
    CONTRADICTION = "contradiction"
    BLOCKED_PATH = "blocked_path"
    SUCCESS = "success"
    CAPABILITY = "capability"
    STRATEGY = "strategy"
    PROMOTED_PATTERN = "promoted_pattern"

@dataclass(frozen=True)
class OmegaMemoryRecord:
    record_id: str
    polarity: MemoryPolarity
    kind: MemoryRecordKind
    title: str
    context: str
    cause: str
    lesson: str
    linked_node_refs: list[str]
    reusable_rule: str | None = None

@dataclass(frozen=True)
class OmegaLearningSignal:
    source_record_id: str
    recommendation: str
    avoid_pattern: str | None
    reuse_pattern: str | None
    target_layer: str


def signal_from_memory(record: OmegaMemoryRecord) -> OmegaLearningSignal:
    if record.polarity == MemoryPolarity.NEGATIVE:
        return OmegaLearningSignal(
            source_record_id=record.record_id,
            recommendation="reduce recurrence of this failure mode before expanding related nodes",
            avoid_pattern=record.lesson,
            reuse_pattern=None,
            target_layer="OmegaGovernance/OmegaQuestion/OmegaProtocol",
        )
    return OmegaLearningSignal(
        source_record_id=record.record_id,
        recommendation="reuse this successful pattern when similar frontiers appear",
        avoid_pattern=None,
        reuse_pattern=record.reusable_rule or record.lesson,
        target_layer="OmegaResearch/OmegaProtocol/OmegaPromotion",
    )


def signals_from_memory(records: list[OmegaMemoryRecord]) -> list[OmegaLearningSignal]:
    return [signal_from_memory(record) for record in records]


def write_memory_records(records: list[OmegaMemoryRecord], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(record) for record in records], indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def write_learning_signals(signals: list[OmegaLearningSignal], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(signal) for signal in signals], indent=2, ensure_ascii=False), encoding="utf-8")
    return path
