from tfuga.historical_replay import AITHistoricalReplay


def test_historical_replay_defaults():
    replay = AITHistoricalReplay()
    results = replay.run_all(replay.demo_points())
    assert len(results) >= 4
    assert all(result.name for result in results)
