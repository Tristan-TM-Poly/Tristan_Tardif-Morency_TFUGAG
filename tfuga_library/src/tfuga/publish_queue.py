from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PublishDraft:
    name: str
    channel: str
    title: str
    body: str
    gates: tuple[str, ...]


class AITPublishQueue:
    gates = ("identity", "permission", "contact", "optout", "review")

    def default_drafts(self) -> tuple[PublishDraft, ...]:
        return (
            PublishDraft("tfuga", "email", "TFUGA update", "TFUGA/OAK stack update: research to verified artifacts.", self.gates),
            PublishDraft("oak", "post", "OAK update", "OAK readiness and verification workflow update.", ("review", "accuracy")),
            PublishDraft("ait", "email", "AIT update", "AIT venture and research automation update.", self.gates),
            PublishDraft("hgfm", "post", "HGFM update", "HGFM graph/fractal/tensor research note.", ("review", "accuracy")),
        )

    def markdown(self) -> str:
        lines = ["# AIT Publish Queue", "", "mode: draft_only", ""]
        for draft in self.default_drafts():
            lines.append(f"## {draft.name} / {draft.channel}")
            lines.append(f"- title: `{draft.title}`")
            lines.append(f"- gates: `{', '.join(draft.gates)}`")
            lines.append(draft.body)
            lines.append("")
        return "\n".join(lines).strip() + "\n"
