"""TFUGAG Fractal Atlas Engine.

Builds nested atlas nodes around a focus. Each focus can expand into lenses:
sources, claims, questions, experiments, applications, risks, contradictions,
and bridges. The engine produces a navigable structure only; it does not mutate
canon or fetch external data.
"""
from dataclasses import dataclass, asdict
import json
from pathlib import Path

LENSES = [
    "sources",
    "claims",
    "questions",
    "experiments",
    "applications",
    "risks",
    "contradictions",
    "bridges",
]

@dataclass(frozen=True)
class FractalAtlasNode:
    node_id: str
    title: str
    depth: int
    lens: str
    children: list


def expand_focus(focus_id: str, title: str, max_depth: int = 2, depth: int = 0, lens: str = "root") -> dict:
    if depth >= max_depth:
        return asdict(FractalAtlasNode(focus_id, title, depth, lens, []))

    children = []
    for child_lens in LENSES:
        child_id = f"{focus_id}.{child_lens}"
        child_title = f"{title} / {child_lens}"
        children.append(expand_focus(child_id, child_title, max_depth, depth + 1, child_lens))

    return asdict(FractalAtlasNode(focus_id, title, depth, lens, children))


def write_fractal_atlas(root: dict, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(root, indent=2, ensure_ascii=False), encoding="utf-8")
    return path
