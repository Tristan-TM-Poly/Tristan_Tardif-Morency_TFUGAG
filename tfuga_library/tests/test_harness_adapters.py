from tfuga import AgentAction, AgentHarnessAdapter, DeliveryHarnessAdapter, DeliverySignal, LocalAICouncilAdapter, ModelAnswer


def test_local_ai_council_selects_best_answer():
    decision = LocalAICouncilAdapter().decide([
        ModelAnswer("small", "ok", 0.4, cost_hint=0.2, latency_hint=0.2),
        ModelAnswer("strong", "detailed and useful answer", 0.9, cost_hint=1.0, latency_hint=1.0),
    ])
    assert decision.winner.model_id in {"small", "strong"}
    assert decision.oak_score > 0


def test_delivery_harness_scores_quality():
    assessment = DeliveryHarnessAdapter().assess(DeliverySignal(changed_files=5, additions=200, tests_added=3, docs_added=1))
    assert assessment.risk in {"low", "medium", "high"}
    assert "tests" in assessment.required_gates


def test_agent_harness_rejects_unknown_action():
    trace = AgentHarnessAdapter().filter_actions([AgentAction("read", "inspect"), AgentAction("unknown", "not allowed")])
    assert len(trace.accepted) == 1
    assert len(trace.rejected) == 1
