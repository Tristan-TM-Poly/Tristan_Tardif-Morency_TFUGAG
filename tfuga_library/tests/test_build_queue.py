from tfuga.build_queue import AITBuildQueue


def test_build_queue_demo_plans():
    q = AITBuildQueue()
    plans = q.queue(q.demo_needs())
    assert len(plans) >= 3
    assert all(plan.score == 10.0 for plan in plans)
    assert "dry_run" in q.markdown(plans)
