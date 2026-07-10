from tfuga.mycelial_action import MycelialEdge, NodeState, SedenionicMycelialAction, demo


def test_mycelial_action_demo_and_relax():
    engine = SedenionicMycelialAction()
    traj, edges = demo()
    assert isinstance(engine.action(traj, edges), float)
    assert "discrete_variational_prototype" in engine.markdown(traj, edges)
    states = (NodeState("a", (0.0,) * 16, 1, 1, 0), NodeState("b", (2.0,) + (0.0,) * 15, 1, 1, 0))
    e = (MycelialEdge("a", "b"),)
    assert engine.tension(engine.relax(states, e, 0.25), e) < engine.tension(states, e)
