from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EmailStatus(str, Enum):
    BLOCKED = "blocked"
    READY_FOR_REVIEW = "ready_for_review"


@dataclass(frozen=True)
class CompanyProfile:
    name: str
    domain: str
    sender_name: str
    sender_email: str
    postal_address: str = ""
    jurisdiction: str = "CA"


@dataclass(frozen=True)
class Recipient:
    email: str
    name: str = ""
    consent: bool = False
    suppressed: bool = False
    source: str = ""


@dataclass(frozen=True)
class EmailDraft:
    company: CompanyProfile
    recipient: Recipient
    subject: str
    body: str
    status: EmailStatus
    blockers: tuple[str, ...]
    oak_score: float


class AITEmailsPublishingManager:
    def blockers(self, company: CompanyProfile, recipient: Recipient, subject: str, body: str) -> tuple[str, ...]:
        issues = []
        if not recipient.email or "@" not in recipient.email:
            issues.append("invalid recipient email")
        if recipient.suppressed:
            issues.append("recipient suppressed")
        if not recipient.consent:
            issues.append("missing consent")
        if not company.sender_email or "@" not in company.sender_email:
            issues.append("missing sender identity")
        if not company.postal_address:
            issues.append("missing postal address")
        if not subject.strip():
            issues.append("missing subject")
        if not body.strip():
            issues.append("missing body")
        if "unsubscribe" not in body.lower() and "opt-out" not in body.lower():
            issues.append("missing unsubscribe language")
        return tuple(issues)

    def oak_score(self, blockers: tuple[str, ...]) -> float:
        return round(max(0.0, 10.0 - 1.7 * len(blockers)), 4)

    def draft(self, company: CompanyProfile, recipient: Recipient, subject: str, message: str) -> EmailDraft:
        body = message.rstrip() + f"\n\n--\n{company.sender_name}\n{company.name}\n{company.postal_address}\nTo unsubscribe or opt out, reply with UNSUBSCRIBE."
        blockers = self.blockers(company, recipient, subject, body)
        status = EmailStatus.BLOCKED if blockers else EmailStatus.READY_FOR_REVIEW
        return EmailDraft(company, recipient, subject.strip(), body, status, blockers, self.oak_score(blockers))


@dataclass(frozen=True)
class BusinessAsset:
    name: str
    company: str
    category: str
    value_score: float
    proof_score: float
    risk_score: float
    revenue_potential: float
    next_action: str


class AITBusinessManager:
    def asset_score(self, asset: BusinessAsset) -> float:
        benefit = asset.value_score * .3 + asset.proof_score * .25 + asset.revenue_potential * .3
        safety = max(0, 1 - asset.risk_score) * .15
        return round(10 * max(0, benefit + safety), 4)

    def rank(self, assets: tuple[BusinessAsset, ...]) -> tuple[BusinessAsset, ...]:
        return tuple(sorted(assets, key=self.asset_score, reverse=True))

    def markdown(self, assets: tuple[BusinessAsset, ...]) -> str:
        ranked = self.rank(assets)
        lines = ["# AIT Business Manager", "", "mode: company_pipeline_oak", ""]
        for asset in ranked:
            lines.append(f"- `{asset.company}` / `{asset.name}` score `{self.asset_score(asset)}` next `{asset.next_action}`")
        lines.append("OAK invariant: company -> asset -> score -> pipeline -> draft/legal/finance handoff")
        return "\n".join(lines) + "\n"


def demo_assets() -> tuple[BusinessAsset, ...]:
    return (
        BusinessAsset("TFUGA Python Library", "TFUGA Labs", "software", .9, .8, .25, .85, "prepare demo + pricing page"),
        BusinessAsset("Email Publishing Manager", "AIT Systems", "go-to-market", .85, .75, .4, .9, "build consented draft campaign"),
    )
