"""TFUGAG Protocol Registry.

Records reviewable research protocols, expected inputs, expected outputs,
result artifacts, and evidence links. This registry is descriptive only: it does
not run code, deploy systems, push branches, or perform external operations.
"""
from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

class ProtocolStatus(str, Enum):
    PROPOSED = "proposed"
    READY_FOR_REVIEW = "ready_for_review"
    COMPLETED = "completed"
    INCONCLUSIVE = "inconclusive"
    BLOCKED = "blocked"

@dataclass(frozen=True)
class ResearchProtocol:
    protocol_id: str
    title: str
    objective: str
    required_inputs: list[str]
    expected_outputs: list[str]
    safety_constraints: list[str]
    review_notes: list[str]

@dataclass(frozen=True)
class ProtocolRecord:
    protocol_id: str
    status: ProtocolStatus
    output_refs: list[str]
    evidence_refs: list[str]
    notes: str


def validate_protocol(protocol: ResearchProtocol) -> list[str]:
    issues = []
    if not protocol.objective.strip():
        issues.append("objective is missing")
    if not protocol.required_inputs:
        issues.append("required inputs are missing")
    if not protocol.expected_outputs:
        issues.append("expected outputs are missing")
    if not protocol.safety_constraints:
        issues.append("safety constraints are missing")
    return issues


def write_protocol_record(record: ProtocolRecord, output_dir: str | Path = "protocols/records") -> Path:
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{record.protocol_id}.json"
    path.write_text(json.dumps(asdict(record), indent=2, ensure_ascii=False), encoding="utf-8")
    return path
