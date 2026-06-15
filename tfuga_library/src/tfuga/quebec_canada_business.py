from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class GateStatus(str, Enum):
    PASS = "pass"
    BLOCK = "block"
    REVIEW = "review"


@dataclass(frozen=True)
class JurisdictionGate:
    key: str
    region: str
    status: GateStatus
    reason: str
    next_action: str


@dataclass(frozen=True)
class CompanyQC:
    name: str
    legal_form: str
    has_neq: bool = False
    has_cra_bn: bool = False
    gst_qst_registered: bool = False
    permits_checked: bool = False
    consent_registry_ready: bool = False
    privacy_review_ready: bool = False


@dataclass(frozen=True)
class FundingRoute:
    name: str
    region: str
    fit_score: float
    next_action: str


class AITQuebecCanadaBusinessManager:
    def gates(self, company: CompanyQC) -> tuple[JurisdictionGate, ...]:
        return (
            JurisdictionGate("req_neq", "Quebec", GateStatus.PASS if company.has_neq else GateStatus.BLOCK, "NEQ/status confirmed" if company.has_neq else "NEQ/status not confirmed", "Search/confirm enterprise in Registraire des entreprises."),
            JurisdictionGate("cra_bn", "Canada", GateStatus.PASS if company.has_cra_bn else GateStatus.REVIEW, "CRA BN confirmed" if company.has_cra_bn else "CRA BN not confirmed", "Determine whether BN/program accounts are required."),
            JurisdictionGate("gst_qst", "Canada/Quebec", GateStatus.PASS if company.gst_qst_registered else GateStatus.REVIEW, "tax registrations confirmed" if company.gst_qst_registered else "GST/HST/QST status not confirmed", "Check small supplier and registration status."),
            JurisdictionGate("permits", "Canada/Quebec/Municipal", GateStatus.PASS if company.permits_checked else GateStatus.REVIEW, "permits checked" if company.permits_checked else "permits/licences not checked", "Run official permit/licence scan."),
            JurisdictionGate("casl", "Canada", GateStatus.PASS if company.consent_registry_ready else GateStatus.BLOCK, "consent controls ready" if company.consent_registry_ready else "commercial emailing needs consent controls", "Keep outbound email draft-only until consent evidence exists."),
            JurisdictionGate("privacy", "Canada/Quebec", GateStatus.PASS if company.privacy_review_ready else GateStatus.REVIEW, "privacy review ready" if company.privacy_review_ready else "privacy/data handling review not confirmed", "Document data purpose, retention and deletion process."),
        )

    def funding_routes(self) -> tuple[FundingRoute, ...]:
        routes = (
            FundingRoute("BDC financing/advisory route", "Canada", .82, "Prepare financing-ready one-pager and projections."),
            FundingRoute("Quebec innovation/growth support route", "Quebec", .80, "Prepare Quebec-focused innovation dossier."),
            FundingRoute("Canada permit/licence readiness route", "Canada", .78, "Run official permit/licence scan before regulated sales."),
            FundingRoute("SR&ED / R&D evidence route", "Canada/Quebec", .76, "Maintain technical logs, hypotheses, experiments and tests."),
        )
        return tuple(sorted(routes, key=lambda r: r.fit_score, reverse=True))

    def oak_score(self, gates: tuple[JurisdictionGate, ...]) -> float:
        gate_score = sum(1 if g.status == GateStatus.PASS else .55 if g.status == GateStatus.REVIEW else 0 for g in gates) / len(gates)
        route_score = sum(r.fit_score for r in self.funding_routes()[:3]) / 3
        return round(10 * (.65 * gate_score + .35 * route_score), 4)

    def markdown(self, company: CompanyQC) -> str:
        gates = self.gates(company)
        lines = ["# AIT Quebec Canada Business Manager", "", "mode: qc_ca_oak_pipeline", "", f"company: `{company.name}`", f"oak_score: `{self.oak_score(gates)}`", ""]
        for gate in gates:
            lines.append(f"- `{gate.key}` region `{gate.region}` status `{gate.status.value}` :: {gate.reason}")
        lines.append("OAK invariant: Quebec/Canada gates -> tax/permit/consent review -> funding route -> draft-only business packet")
        return "\n".join(lines) + "\n"


def demo_company() -> CompanyQC:
    return CompanyQC("TFUGA Labs Quebec", "to-confirm")
