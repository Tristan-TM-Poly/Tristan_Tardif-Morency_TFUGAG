"""TFUGAG Web Ingestion Planner.

Turns approved web tools into bounded ingestion plans. The planner does not
fetch the web itself. It creates reviewable instructions for future connectors
or API clients.
"""
from dataclasses import dataclass, asdict
import json
from pathlib import Path

from src.tfuga_web_tools_registry import WebTool, list_tools

@dataclass(frozen=True)
class WebIngestionPlan:
    tool_name: str
    query: str
    purpose: str
    trust: str
    requires_review: bool
    output_target: str
    next_step: str


def make_plan(tool: WebTool, query: str) -> WebIngestionPlan:
    return WebIngestionPlan(
        tool_name=tool.name,
        query=query,
        purpose=tool.purpose,
        trust=tool.trust.value,
        requires_review=tool.requires_review,
        output_target=f"incoming/web/{tool.name}/",
        next_step="Convert returned metadata into Knowledge Atoms before graph insertion.",
    )


def make_plans(query: str) -> list[WebIngestionPlan]:
    return [make_plan(tool, query) for tool in list_tools()]


def write_plans(plans: list[WebIngestionPlan], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(plan) for plan in plans], indent=2, ensure_ascii=False), encoding="utf-8")
    return path
