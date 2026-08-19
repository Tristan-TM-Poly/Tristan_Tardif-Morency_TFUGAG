from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AlgebraRoute:
    expression: str
    algebra: str
    reason: str


class TGFAAlgebraRouter:
    def route(self, expression: str) -> AlgebraRoute:
        text = expression.lower()
        if "tensor" in text or "⊗" in expression:
            return AlgebraRoute(expression, "tensor", "tensor marker detected")
        if "octonion" in text or "sedenion" in text or "quaternion" in text:
            return AlgebraRoute(expression, "hypercomplex", "named hypercomplex layer detected")
        if "i*" in text or "sqrt(-1)" in text or " I" in expression or "I*" in expression:
            return AlgebraRoute(expression, "complex", "imaginary marker detected")
        if any(ch.isalpha() for ch in expression):
            return AlgebraRoute(expression, "symbolic_real_candidate", "symbolic expression without hyper marker")
        return AlgebraRoute(expression, "numeric_real", "numeric real candidate")
