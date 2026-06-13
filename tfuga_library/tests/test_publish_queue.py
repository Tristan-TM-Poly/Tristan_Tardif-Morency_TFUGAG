from tfuga.publish_queue import AITPublishQueue


def test_publish_queue_markdown():
    q = AITPublishQueue()
    assert len(q.default_drafts()) >= 4
    assert "draft_only" in q.markdown()
