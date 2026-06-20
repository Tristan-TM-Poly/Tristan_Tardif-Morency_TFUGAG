from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TextSection:
    title: str
    body: str


class TextPublisher:
    def render(self, title: str, sections: list[TextSection]) -> str:
        lines = [f"# {title}", ""]
        for section in sections:
            lines.extend([f"## {section.title}", "", section.body.strip(), ""])
        return "\n".join(lines).strip() + "\n"
