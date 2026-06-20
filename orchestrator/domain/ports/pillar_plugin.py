"""
Port: PillarPlugin — Core contract for all analysis pillars.

Every pillar in the decision engine implements this interface.
Plugins are auto-discovered and executed by the PipelineOrchestrator.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class PillarResult:
    """Standardized output from every pillar plugin analysis.

    Attributes:
        pillar_id:     Unique identifier matching the plugin (e.g. 'sre_reliability').
        strategy:      Human-readable strategy label.
        tier:          Decision-tree leaf identifier.
        reasoning:     Explanation of *why* this strategy was chosen.
        details:       Plugin-specific payload (SLIs, tools, thresholds, …).
        audit_entries: Optional list of audit-trail items contributed by this pillar.
    """

    pillar_id: str
    strategy: str
    tier: str
    reasoning: str
    details: Dict[str, Any] = field(default_factory=dict)
    audit_entries: List[Dict[str, Any]] = field(default_factory=list)


class PillarPlugin(ABC):
    """Abstract base contract that every analysis pillar must satisfy.

    Lifecycle
    ---------
    1. The ``PluginRegistry`` discovers and instantiates plugins at startup.
    2. The ``PipelineOrchestrator`` sorts them by ``dependencies`` (topological).
    3. For each plugin, ``analyze(metrics, state)`` is called exactly once.
    4. The returned ``PillarResult`` is stored in ``PipelineState.pillar_results``.
    """

    # ── Identity ────────────────────────────────────────────────────

    @property
    @abstractmethod
    def pillar_id(self) -> str:
        """Globally-unique slug (e.g. ``'sre_reliability'``)."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable display name (e.g. ``'SRE & Reliability Engineering'``)."""
        ...

    @property
    @abstractmethod
    def category(self) -> str:
        """One of: ``'architecture'``, ``'compliance'``, ``'operations'``,
        ``'performance'``, ``'engineering'``, ``'product'``,
        ``'organization'``, ``'financial'``."""
        ...

    @property
    def version(self) -> str:
        """SemVer version of this plugin."""
        return "1.0.0"

    # ── Ordering ────────────────────────────────────────────────────

    @property
    def dependencies(self) -> List[str]:
        """``pillar_id`` values that must execute before this plugin.

        Return an empty list (default) if the plugin has no ordering
        constraints.
        """
        return []

    @property
    def priority(self) -> int:
        """Lower numbers execute first within the same dependency tier.

        Default is ``100``; override to adjust relative ordering among
        peers with identical dependency sets.
        """
        return 100

    # ── Core Logic ──────────────────────────────────────────────────

    @abstractmethod
    def analyze(
        self,
        metrics: Dict[str, Any],
        state: Any,  # PipelineState — forward reference avoids circular import
    ) -> PillarResult:
        """Run the pillar analysis and return a deterministic result.

        Parameters
        ----------
        metrics:
            Pre-computed runtime metrics dictionary (traffic, compliance
            flags, scaling indicators, …).
        state:
            The current ``PipelineState`` snapshot.  Plugins should treat
            it as **read-only** — the orchestrator is responsible for
            integrating results back into the state.

        Returns
        -------
        PillarResult
            Immutable result dataclass with strategy, tier, reasoning,
            and plugin-specific details.
        """
        ...
