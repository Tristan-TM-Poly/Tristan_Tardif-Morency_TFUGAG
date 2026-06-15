from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


def _add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def _sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def _neg(x):
    return tuple(-a for a in x)


def _conj(x):
    if len(x) == 1:
        return x
    h = len(x) // 2
    return _conj(x[:h]) + _neg(x[h:])


def _mul(x, y):
    n = len(x)
    if n == 1:
        return (x[0] * y[0],)
    h = n // 2
    a, b = x[:h], x[h:]
    c, d = y[:h], y[h:]
    return _sub(_mul(a, c), _mul(d, _conj(b))) + _add(_mul(_conj(a), d), _mul(c, b))


@dataclass(frozen=True)
class Sedenion:
    coeffs: tuple[float, ...]

    def __post_init__(self):
        if len(self.coeffs) != 16:
            raise ValueError("need 16 coefficients")

    @staticmethod
    def basis(i: int) -> "Sedenion":
        data = [0.0] * 16
        data[i] = 1.0
        return Sedenion(tuple(data))

    @staticmethod
    def zero() -> "Sedenion":
        return Sedenion((0.0,) * 16)

    def __add__(self, other: "Sedenion") -> "Sedenion":
        return Sedenion(_add(self.coeffs, other.coeffs))

    def __sub__(self, other: "Sedenion") -> "Sedenion":
        return Sedenion(_sub(self.coeffs, other.coeffs))

    def __mul__(self, other: "Sedenion") -> "Sedenion":
        return Sedenion(_mul(self.coeffs, other.coeffs))

    def conj(self) -> "Sedenion":
        return Sedenion(_conj(self.coeffs))

    def norm2(self) -> float:
        return sum(v * v for v in self.coeffs)

    def norm(self) -> float:
        return sqrt(self.norm2())

    def is_zero(self, tol: float = 1e-12) -> bool:
        return all(abs(v) <= tol for v in self.coeffs)


def associator(a: Sedenion, b: Sedenion, c: Sedenion) -> Sedenion:
    return (a * b) * c - a * (b * c)


def known_zero_divisor_pair() -> tuple[Sedenion, Sedenion]:
    return Sedenion.basis(1) + Sedenion.basis(10), Sedenion.basis(6) - Sedenion.basis(13)


def norm_defect(a: Sedenion, b: Sedenion) -> float:
    return round((a * b).norm2() - a.norm2() * b.norm2(), 12)


def oak_warning() -> str:
    return "sedenions are non-associative and contain zero divisors; use OAK gates before physics claims"
