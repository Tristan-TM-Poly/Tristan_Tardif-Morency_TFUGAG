from tfuga import AITRouteSelector, RouteGoal


def test_repo_route():
    plan = AITRouteSelector().plan(RouteGoal("repo", "repo", "github"))
    assert "draft PR" in plan.route
    assert plan.oak_score >= 8


def test_adapter_route():
    plan = AITRouteSelector().plan(RouteGoal("adapter", "adapter", "api"))
    assert "adapter" in plan.route


def test_review_route():
    plan = AITRouteSelector().plan(RouteGoal("review", "review", "queue"))
    assert "review" in plan.route


def test_markdown_report():
    selector = AITRouteSelector()
    report = selector.markdown(selector.plan_many(selector.default_goals()))
    assert "AIT Route Selector Report" in report
    assert "Repository package update" in report
