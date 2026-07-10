from tfuga.universal_replay import AITUniversalReplay


def test_universal_replay_runs_defaults():
    replay = AITUniversalReplay()
    outcomes = replay.run_all(replay.demo_tasks())
    assert len(outcomes) >= 3
    assert all(outcome.total_score for outcome in outcomes)
