from tfuga import AITCapabilityAbsorber, CapabilityCard


def test_absorber_plans_permissive_capability():
    card = CapabilityCard(
        name="MCP tool protocol",
        source="public ecosystem",
        license_name="open-standard",
        capability="standardized tools resources prompts interface",
        pattern="adapter_protocol",
    )
    plan = AITCapabilityAbsorber().plan(card)
    assert plan.allowed
    assert plan.oak_score >= 8.0
    assert "adapter" in plan.adapter_name


def test_absorber_flags_unknown_license_as_review_required():
    card = CapabilityCard(
        name="Unknown repo pattern",
        source="github",
        license_name="unknown",
        capability="workflow idea",
        pattern="metadata_only",
    )
    plan = AITCapabilityAbsorber().plan(card)
    assert plan.allowed
    assert "license review" in plan.reason


def test_absorber_writes_markdown_and_checklist():
    cards = [
        CapabilityCard("LangGraph-style graph workflow", "public docs", "MIT", "stateful graph orchestration", "graph_adapter"),
        CapabilityCard("Crew-style roles", "public docs", "MIT", "multi-agent role/task pattern", "role_adapter"),
    ]
    absorber = AITCapabilityAbsorber()
    report = absorber.markdown_report(cards)
    checklist = absorber.proposal_checklist(cards)
    assert "AIT Capability Absorption Report" in report
    assert "LangGraph-style" in report
    assert "[ ]" in checklist
