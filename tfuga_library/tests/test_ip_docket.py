from tfuga.ip_docket import AITIPDocket, IPDisclosure


def test_ip_docket_plan_and_markdown():
    item = IPDisclosure("demo", "AI workflow", "fragmented process", "gated packet", ("inventor",), ("Canada", "PCT"))
    docket = AITIPDocket()
    plan = docket.plan(item, "CIPO")
    assert plan.readiness > 0
    assert "official" in plan.gates[-1]
    assert "AIT IP Docket" in docket.markdown(item)


def test_pct_route_mentions_epct():
    item = IPDisclosure("demo", "AI", "p", "s", ("i",), ("PCT",))
    plan = AITIPDocket().plan(item, "PCT")
    assert "ePCT" in plan.handoff
