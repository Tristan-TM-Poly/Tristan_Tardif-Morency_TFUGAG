from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class QuebecResearchCard:
    institution: str
    domain: str
    capability: str
    source_hint: str
    oak_level: int = 3


@dataclass(frozen=True)
class QuebecSynergy:
    title: str
    institutions: tuple[str, ...]
    tfuga_adapter: str
    expected_gain: float
    proposal: str
    gates: tuple[str, ...]


class AITQuebecResearchAbsorber:
    """Absorb public Quebec university research themes into TFUGA proposals."""

    def default_cards(self) -> tuple[QuebecResearchCard, ...]:
        return (
            QuebecResearchCard("Université de Montréal / Mila", "AI + data + health + social impact", "AI research support, responsible research, digital research support, valorization", "public research portal", 5),
            QuebecResearchCard("McGill", "research support + innovation + compliance", "research support hub, innovation partnerships, ethics/compliance, strategic research planning", "public research portal", 5),
            QuebecResearchCard("Université Laval", "northern research + transdisciplinary innovation", "300+ units/chairs/centres and Arctic/North expertise", "public research portal", 5),
            QuebecResearchCard("Université de Sherbrooke", "quantum + health + climate + aging + partnerships", "federating themes, quantum institute, health, sustainability, partnership research", "public research portal", 5),
            QuebecResearchCard("Polytechnique Montréal", "engineering + quantum + partnerships", "research units, industry partnerships, responsible research, infrastructure access", "public research portal", 5),
            QuebecResearchCard("INRS", "water + energy + materials + health + urban systems", "graduate research centers and applied mission", "public institutional profile", 4),
            QuebecResearchCard("Concordia", "sustainability + society + digital innovation", "research portal and cross-domain collaboration", "public research portal", 4),
            QuebecResearchCard("UQAM", "society + environment + culture + health", "research and creation portal, social/environmental strengths", "public research portal", 4),
            QuebecResearchCard("ETS", "applied engineering + industry transfer", "engineering research, partnerships and applied technology transfer", "public research portal", 4),
            QuebecResearchCard("HEC Montréal", "management + data + organizations", "business research, analytics and organizational innovation", "public research portal", 4),
        )

    def score_card(self, card: QuebecResearchCard) -> float:
        score = float(card.oak_level)
        text = f"{card.domain} {card.capability}".lower()
        if "ai" in text or "data" in text or "digital" in text:
            score += 1.0
        if "health" in text or "sant" in text:
            score += 0.7
        if "quantum" in text or "materials" in text:
            score += 0.7
        if "environment" in text or "climate" in text or "water" in text or "north" in text:
            score += 0.7
        if "partnership" in text or "innovation" in text or "transfer" in text:
            score += 0.6
        return round(min(score, 10.0), 2)

    def build_synergies(self, cards: Iterable[QuebecResearchCard]) -> tuple[QuebecSynergy, ...]:
        cards = tuple(cards)
        by_domain = " ".join(card.domain.lower() + " " + card.capability.lower() for card in cards)
        synergies: list[QuebecSynergy] = []
        if "ai" in by_domain or "data" in by_domain:
            synergies.append(QuebecSynergy("AI/OAK Research Cartographer", ("Université de Montréal / Mila", "McGill", "Polytechnique Montréal", "HEC Montréal"), "QuebecAIResearchAdapter", 9.0, "Map Quebec AI/data strengths into TFUGA capability cards, OAK gates, and proposal queues.", ("source_cards", "license_check", "adapter", "tests", "docs", "draft_pr")))
        if "quantum" in by_domain or "materials" in by_domain:
            synergies.append(QuebecSynergy("Quantum-Materials Genesis Loop", ("Université de Sherbrooke", "Polytechnique Montréal", "INRS"), "QuantumMaterialsAdapter", 8.7, "Generate safe research proposals linking quantum, materials, energy and simulation layers.", ("source_cards", "theory_stub", "simulation_plan", "tests", "docs")))
        if "health" in by_domain:
            synergies.append(QuebecSynergy("Health + Aging + Precision OAK Loop", ("Université de Sherbrooke", "Université de Montréal / Mila", "INRS", "UQAM"), "HealthSocietyAdapter", 8.4, "Convert health, aging and society themes into ethical, privacy-aware research automation plans.", ("ethics_gate", "privacy_boundary", "adapter", "tests", "docs")))
        if "environment" in by_domain or "climate" in by_domain or "water" in by_domain or "north" in by_domain:
            synergies.append(QuebecSynergy("Climate-Water-North Digital Twin", ("Université Laval", "INRS", "Université de Sherbrooke", "UQAM"), "EcoNorthWaterAdapter", 8.8, "Build graphable environmental/northern/water systems into TFUGA simulation and report pipelines.", ("source_cards", "data_boundary", "model_plan", "tests", "docs")))
        if "partnership" in by_domain or "transfer" in by_domain or "innovation" in by_domain:
            synergies.append(QuebecSynergy("Research-to-Prototype Transfer Engine", ("Polytechnique Montréal", "ETS", "McGill", "Université Laval"), "PrototypeTransferAdapter", 8.6, "Turn public research capabilities into prototypes, issues, draft PRs, documentation and validation plans.", ("partner_boundary", "proposal", "artifact", "tests", "docs", "draft_pr")))
        return tuple(synergies)

    def markdown_report(self, cards: Iterable[QuebecResearchCard]) -> str:
        cards = tuple(cards)
        synergies = self.build_synergies(cards)
        lines = ["# AIT Quebec Research Absorber Report", "", "## Research capability cards", ""]
        for card in cards:
            lines.append(f"- `{card.institution}` — {card.domain}; score `{self.score_card(card)}`; capability: {card.capability}")
        lines.extend(["", "## TFUGA/OAK synergies", ""])
        for item in synergies:
            lines.append(f"### {item.title}")
            lines.append(f"- institutions: `{', '.join(item.institutions)}`")
            lines.append(f"- adapter: `{item.tfuga_adapter}`")
            lines.append(f"- expected gain: `{item.expected_gain}`")
            lines.append(f"- proposal: {item.proposal}")
            lines.append(f"- gates: `{', '.join(item.gates)}`")
            lines.append("")
        return "\n".join(lines).strip() + "\n"

    def proposal_checklist(self, cards: Iterable[QuebecResearchCard]) -> str:
        lines = ["# Quebec Research Improvement Checklist", ""]
        for synergy in self.build_synergies(cards):
            lines.append(f"## {synergy.title}")
            lines.append(f"- [ ] Create `{synergy.tfuga_adapter}`")
            lines.append("- [ ] Add source cards and citations")
            lines.append("- [ ] Add OAK tests")
            lines.append("- [ ] Add documentation")
            lines.append("- [ ] Open or update draft PR")
            lines.append("")
        return "\n".join(lines).strip() + "\n"
