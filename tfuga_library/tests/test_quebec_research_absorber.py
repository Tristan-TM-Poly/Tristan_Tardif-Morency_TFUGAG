from tfuga import AITQuebecResearchAbsorber, QuebecResearchCard


def test_default_cards_exist():
    cards = AITQuebecResearchAbsorber().default_cards()
    assert len(cards) >= 8


def test_scores_prioritize_ai_and_partnerships():
    absorber = AITQuebecResearchAbsorber()
    card = QuebecResearchCard("X", "AI health innovation", "data partnership", "public")
    assert absorber.score_card(card) > 4


def test_synergies_generated():
    absorber = AITQuebecResearchAbsorber()
    synergies = absorber.build_synergies(absorber.default_cards())
    assert len(synergies) >= 4
    assert any("AI" in item.title for item in synergies)


def test_markdown_and_checklist():
    absorber = AITQuebecResearchAbsorber()
    report = absorber.markdown_report(absorber.default_cards())
    checklist = absorber.proposal_checklist(absorber.default_cards())
    assert "AIT Quebec Research Absorber Report" in report
    assert "[ ]" in checklist
