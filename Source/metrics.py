"""Shared result and metrics helpers for solver comparisons."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class SolverStats:
    method: str
    runtime: float = 0.0
    nodes_expanded: int = 0
    assignments_tried: int = 0
    inferences: int = 0
    contradictions: int = 0
    max_frontier: int = 0

    def as_dict(self) -> Dict[str, object]:
        return {
            "method": self.method,
            "runtime": self.runtime,
            "nodes_expanded": self.nodes_expanded,
            "assignments_tried": self.assignments_tried,
            "inferences": self.inferences,
            "contradictions": self.contradictions,
            "max_frontier": self.max_frontier,
        }


@dataclass
class SolverResult:
    grid: Optional[List[List[int]]]
    stats: SolverStats = field(default_factory=lambda: SolverStats("unknown"))

