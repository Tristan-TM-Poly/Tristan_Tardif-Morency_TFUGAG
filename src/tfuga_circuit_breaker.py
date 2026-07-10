"""Local circuit breaker utilities for TFUGAG review pipelines.

The breaker limits how many generated review items can be staged during a time
window. This protects the repository from noisy bursts and keeps review work
human-scale.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import time


@dataclass
class CircuitBreaker:
    max_events: int = 20
    window_seconds: int = 3600
    timestamps: list[float] = field(default_factory=list)

    def allow(self, now: float | None = None) -> bool:
        current = time.time() if now is None else now
        cutoff = current - self.window_seconds
        self.timestamps = [stamp for stamp in self.timestamps if stamp >= cutoff]
        if len(self.timestamps) >= self.max_events:
            return False
        self.timestamps.append(current)
        return True

    def remaining(self, now: float | None = None) -> int:
        current = time.time() if now is None else now
        cutoff = current - self.window_seconds
        self.timestamps = [stamp for stamp in self.timestamps if stamp >= cutoff]
        return max(0, self.max_events - len(self.timestamps))

    def reset(self) -> None:
        self.timestamps.clear()
