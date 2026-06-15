from __future__ import annotations

from dataclasses import dataclass

Vector16 = tuple[float, ...]


def check(v: Vector16) -> Vector16:
    if len(v) != 16:
        raise ValueError("expected 16D")
    return tuple(float(x) for x in v)


def add(a: Vector16, b: Vector16) -> Vector16:
    return tuple(x + y for x, y in zip(check(a), check(b)))


def sub(a: Vector16, b: Vector16) -> Vector16:
    return tuple(x - y for x, y in zip(check(a), check(b)))


def scale(a: Vector16, k: float) -> Vector16:
    return tuple(k * x for x in check(a))


def norm2(a: Vector16) -> float:
    return sum(x * x for x in check(a))


@dataclass(frozen=True)
class NodeState:
    node: str
    value: Vector16
    proof: float = 0.0
    fertility: float = 0.0
    risk: float = 0.0


@dataclass(frozen=True)
class MycelialEdge:
    left: str
    right: str
    weight: float = 1.0


@dataclass(frozen=True)
class ActionTerms:
    kinetic: float
    tension: float
    oak_residue: float
    reward: float
    lagrangian: float


class SedenionicMycelialAction:
    def by_node(self, states: tuple[NodeState, ...]) -> dict[str, NodeState]:
        return {s.node: s for s in states}

    def kinetic(self, prev: tuple[NodeState, ...], cur: tuple[NodeState, ...]) -> float:
        p = self.by_node(prev)
        return round(sum(0.5 * norm2(sub(c.value, p[c.node].value)) for c in cur if c.node in p), 6)

    def tension(self, states: tuple[NodeState, ...], edges: tuple[MycelialEdge, ...]) -> float:
        s = self.by_node(states)
        total = 0.0
        for e in edges:
            if e.left in s and e.right in s:
                total += 0.5 * e.weight * norm2(sub(s[e.left].value, s[e.right].value))
        return round(total, 6)

    def oak_residue(self, states: tuple[NodeState, ...]) -> float:
        return round(sum(max(0.0, 1 - s.proof) ** 2 + max(0.0, s.risk) ** 2 for s in states), 6)

    def reward(self, states: tuple[NodeState, ...]) -> float:
        return round(sum(max(0.0, s.fertility) for s in states), 6)

    def terms(self, prev: tuple[NodeState, ...], cur: tuple[NodeState, ...], edges: tuple[MycelialEdge, ...]) -> ActionTerms:
        k = self.kinetic(prev, cur)
        g = self.tension(cur, edges)
        r = self.oak_residue(cur)
        y = self.reward(cur)
        return ActionTerms(k, g, r, y, round(k - g - r + y, 6))

    def action(self, traj: tuple[tuple[NodeState, ...], ...], edges: tuple[MycelialEdge, ...]) -> float:
        return round(sum(self.terms(traj[i - 1], traj[i], edges).lagrangian for i in range(1, len(traj))), 6)

    def relax(self, states: tuple[NodeState, ...], edges: tuple[MycelialEdge, ...], rate: float = 0.1) -> tuple[NodeState, ...]:
        s = self.by_node(states)
        nudges = {x.node: (0.0,) * 16 for x in states}
        weights = {x.node: 0.0 for x in states}
        for e in edges:
            if e.left in s and e.right in s:
                delta = sub(s[e.right].value, s[e.left].value)
                nudges[e.left] = add(nudges[e.left], scale(delta, e.weight))
                nudges[e.right] = add(nudges[e.right], scale(delta, -e.weight))
                weights[e.left] += e.weight
                weights[e.right] += e.weight
        out = []
        for x in states:
            w = max(weights[x.node], 1e-12)
            out.append(NodeState(x.node, add(x.value, scale(nudges[x.node], rate / w)), x.proof, x.fertility, x.risk))
        return tuple(out)

    def blockers(self, states: tuple[NodeState, ...]) -> tuple[str, ...]:
        out = []
        for s in states:
            if s.proof < 0.5:
                out.append(f"{s.node}: low proof")
            if s.risk > 0.5:
                out.append(f"{s.node}: high risk")
        return tuple(out)

    def markdown(self, traj: tuple[tuple[NodeState, ...], ...], edges: tuple[MycelialEdge, ...]) -> str:
        lines = ["# Sedenionic Mycelial Least Action", "", "mode: discrete_variational_prototype", ""]
        lines.append(f"- total_action: `{self.action(traj, edges)}`")
        lines.append("OAK invariant: 16D trajectory -> action terms -> blockers -> relaxation proposal")
        return "\n".join(lines) + "\n"


def demo() -> tuple[tuple[tuple[NodeState, ...], ...], tuple[MycelialEdge, ...]]:
    a0 = NodeState("theory", (0.0,) * 16, proof=0.4, fertility=0.8, risk=0.2)
    b0 = NodeState("prototype", (1.0,) + (0.0,) * 15, proof=0.7, fertility=0.6, risk=0.1)
    a1 = NodeState("theory", (0.2,) + (0.0,) * 15, proof=0.5, fertility=0.9, risk=0.15)
    b1 = NodeState("prototype", (0.8,) + (0.0,) * 15, proof=0.75, fertility=0.7, risk=0.1)
    return ((a0, b0), (a1, b1)), (MycelialEdge("theory", "prototype"),)
