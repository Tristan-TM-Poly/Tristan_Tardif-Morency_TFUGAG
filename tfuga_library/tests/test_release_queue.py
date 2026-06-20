from tfuga.release_queue import AITReleaseQueue


def test_release_queue_items_and_markdown():
    q = AITReleaseQueue()
    assert len(q.items()) >= 4
    assert "draft_only" in q.markdown()
    assert q.calendar()[0].startswith("day 1")
