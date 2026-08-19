from tfuga import AITAutonomousPushRunPublish, PRPPolicy, PRPRequest


def test_default_is_dry_run():
    plan = AITAutonomousPushRunPublish().plan(PRPRequest("push", "push", "branch"))
    assert plan.mode == "dry_run"
    assert "draft_pr" in plan.gates


def test_run_plan_has_tests_and_report():
    plan = AITAutonomousPushRunPublish().plan(PRPRequest("run", "run", "package", evidence=("pytest",)))
    assert "tests" in plan.gates
    assert "report" in plan.gates


def test_publish_plan_requires_artifact_and_review():
    plan = AITAutonomousPushRunPublish().plan(PRPRequest("publish", "publish", "artifact", "medium"))
    assert "artifact" in plan.gates
    assert "review" in plan.gates


def test_ready_mode_when_policy_allows():
    engine = AITAutonomousPushRunPublish(PRPPolicy(dry_run_default=False, min_oak_score=6.0))
    plan = engine.plan(PRPRequest("run", "run", "package", "low", ("pytest", "report")))
    assert plan.mode == "ready"


def test_markdown_report():
    engine = AITAutonomousPushRunPublish()
    report = engine.generate(engine.default_requests())
    assert "AIT Autonomous Push Run Publish Report" in report.markdown
    assert len(report.plans) == 3
