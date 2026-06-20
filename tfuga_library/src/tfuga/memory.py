from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

MemoryKind = Literal["negative", "positive"]


@dataclass(frozen=True)
class MemoryNode:
    id: str
    kind: MemoryKind
    statement: str
    source: str = "unknown"


@dataclass(frozen=True)
class MemoryEdge:
    source: str
    target: str
    relation: str


@dataclass
class MemoryGraph:
    nodes: dict[str, MemoryNode] = field(default_factory=dict)
    edges: list[MemoryEdge] = field(default_factory=list)

    def add_negative(self, node_id: str, statement: str, source: str = "unknown") -> MemoryNode:
        node = MemoryNode(node_id, "negative", statement, source)
        self.nodes[node_id] = node
        return node

    def add_positive(self, node_id: str, statement: str, source: str = "unknown") -> MemoryNode:
        node = MemoryNode(node_id, "positive", statement, source)
        self.nodes[node_id] = node
        return node

    def promote(self, negative_id: str, positive_id: str, lesson: str) -> None:
        if negative_id not in self.nodes:
            raise KeyError(negative_id)
        self.add_positive(positive_id, lesson, source=negative_id)
        self.edges.append(MemoryEdge(negative_id, positive_id, "promotes_to"))

    def unresolved_negative(self) -> list[MemoryNode]:
        promoted = {edge.source for edge in self.edges if edge.relation == "promotes_to"}
        return [node for node in self.nodes.values() if node.kind == "negative" and node.id not in promoted]
