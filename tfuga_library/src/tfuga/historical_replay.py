from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev
from math import sqrt


@dataclass(frozen=True)
class SeriesPoint:
    date: str
    value: float


@dataclass(frozen=True)
class ReplayClone:
    name: str
    kind: str
    fast: int = 3
    slow: int = 8
    threshold: float = 0.0


@dataclass(frozen=True)
class ReplayResult:
    name: str
    total_change: float
    max_drop: float
    volatility: float
    score: float


class AITHistoricalReplay:
    def ma(self, values: tuple[float, ...], window: int, i: int) -> float:
        start = max(0, i - window + 1)
        return mean(values[start : i + 1])

    def signal(self, values: tuple[float, ...], i: int, clone: ReplayClone) -> int:
        if i == 0:
            return 0
        if clone.kind == "momentum":
            r = values[i] / values[i - 1] - 1.0
            return 1 if r > clone.threshold else -1 if r < -clone.threshold else 0
        if clone.kind == "revert":
            gap = values[i] / self.ma(values, clone.slow, i) - 1.0
            return 1 if gap < -abs(clone.threshold) else -1 if gap > abs(clone.threshold) else 0
        if clone.kind == "cross":
            return 1 if self.ma(values, clone.fast, i) > self.ma(values, clone.slow, i) else -1
        if clone.kind == "baseline":
            return 1
        return 0

    def run(self, points: tuple[SeriesPoint, ...], clone: ReplayClone, cost_bps: float = 10.0) -> ReplayResult:
        if len(points) < 2:
            raise ValueError("Need at least two points.")
        values = tuple(point.value for point in points)
        state = 1.0
        peak = 1.0
        max_drop = 0.0
        pos = 0
        changes = []
        cost = cost_bps / 10000.0
        for i in range(1, len(values)):
            desired = self.signal(values, i - 1, clone)
            if desired != pos:
                state *= 1.0 - cost * abs(desired - pos)
            pos = desired
            step = pos * (values[i] / values[i - 1] - 1.0)
            changes.append(step)
            state *= 1.0 + step
            peak = max(peak, state)
            max_drop = max(max_drop, (peak - state) / peak)
        total = state - 1.0
        vol = pstdev(changes) * sqrt(252) if len(changes) > 1 else 0.0
        score = round(total * 100.0 - max_drop * 80.0 - vol * 10.0, 4)
        return ReplayResult(clone.name, round(total, 6), round(max_drop, 6), round(vol, 6), score)

    def defaults(self) -> tuple[ReplayClone, ...]:
        return (
            ReplayClone("momentum", "momentum", threshold=0.003),
            ReplayClone("cross", "cross", 3, 8),
            ReplayClone("revert", "revert", slow=8, threshold=0.01),
            ReplayClone("baseline", "baseline"),
        )

    def run_all(self, points: tuple[SeriesPoint, ...]) -> tuple[ReplayResult, ...]:
        return tuple(self.run(points, clone) for clone in self.defaults())

    def demo_points(self) -> tuple[SeriesPoint, ...]:
        vals = (100, 101, 102, 100, 99, 101, 103, 104, 102, 105, 107, 106, 108, 110, 109, 111)
        return tuple(SeriesPoint(f"2021-01-{i+1:02d}", value) for i, value in enumerate(vals))
