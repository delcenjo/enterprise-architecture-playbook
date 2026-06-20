"""
Base class for decision-tree-driven pillar plugins.

Provides reusable infrastructure for the ~90% of plugins that follow
the standard pattern: load a decision tree → walk it → return a leaf.
Concrete plugins only need to override ``pillar_id``, ``name``,
``category``, and ``build_question_map()``.
"""

from typing import Any, Callable, Dict, List, Optional

from domain.ports.knowledge_repository import KnowledgeRepository
from domain.ports.pillar_plugin import PillarPlugin, PillarResult
from domain.services.decision_tree_walker import (
    QuestionResolver,
    build_simple_resolver,
    walk_decision_tree,
)


class BaseDecisionTreePlugin(PillarPlugin):
    """Base class for plugins driven by a JSON decision tree.

    Subclasses must implement:
    - ``pillar_id``, ``name``, ``category`` (from PillarPlugin)
    - ``build_question_map(metrics, state)`` — returns mapping of
      node_id → answer-resolver lambdas

    Subclasses may override:
    - ``tree_resource``, ``ontology_resource``, ``cases_resource``,
      ``tradeoff_resource`` — to customize knowledge file names
    - ``default_leaf`` — fallback leaf key
    - ``build_result(leaf, ontology, metrics, state)`` — to customize
      how the PillarResult is constructed from the resolved leaf
    """

    def __init__(
        self,
        knowledge_repo: Optional[KnowledgeRepository] = None,
        **kwargs: Any,
    ) -> None:
        self._knowledge_repo = knowledge_repo

    @property
    def tree_resource(self) -> str:
        """Resource name for the decision tree JSON."""
        return "decision_tree"

    @property
    def ontology_resource(self) -> str:
        """Resource name for the ontology JSON."""
        return "ontology"

    @property
    def cases_resource(self) -> str:
        """Resource name for case studies JSON."""
        return "cases"

    @property
    def tradeoff_resource(self) -> str:
        """Resource name for the tradeoff matrix JSON."""
        return "tradeoff"

    @property
    def default_leaf(self) -> Optional[str]:
        """Fallback leaf key if traversal fails."""
        return None

    def build_question_map(
        self,
        metrics: Dict[str, Any],
        state: Any,
    ) -> Dict[str, Callable[[Dict[str, Any]], str]]:
        """Build the question→answer mapping for decision tree traversal.

        This is the **only logic** each plugin typically needs to implement.

        Parameters
        ----------
        metrics:
            Runtime metrics dictionary.
        state:
            Current pipeline state.

        Returns
        -------
        dict
            Mapping from node_id to a callable that accepts ``metrics``
            and returns the answer string (e.g. ``"yes"`` / ``"no"``).
        """
        raise NotImplementedError(
            f"{type(self).__name__} must implement build_question_map()"
        )

    def analyze(
        self,
        metrics: Dict[str, Any],
        state: Any,
    ) -> PillarResult:
        """Execute the decision-tree-based analysis.

        1. Load knowledge (tree + optionally ontology).
        2. Build question map from subclass.
        3. Walk the tree.
        4. Construct and return a ``PillarResult``.
        """
        if self._knowledge_repo is None:
            raise RuntimeError(
                f"Plugin '{self.pillar_id}' has no KnowledgeRepository. "
                "Ensure it was injected during discovery."
            )

        tree = self._knowledge_repo.load(self.tree_resource)
        ontology = (
            self._knowledge_repo.load(self.ontology_resource)
            if self._knowledge_repo.exists(self.ontology_resource)
            else {}
        )

        question_map = self.build_question_map(metrics, state)
        resolver = build_simple_resolver(question_map, default_answer="no")

        leaf = walk_decision_tree(
            tree,
            question_resolver=resolver,
            metrics=metrics,
            default_leaf_key=self.default_leaf,
        )

        return self.build_result(leaf, ontology, metrics, state)

    def build_result(
        self,
        leaf: Dict[str, Any],
        ontology: Dict[str, Any],
        metrics: Dict[str, Any],
        state: Any,
    ) -> PillarResult:
        """Construct a PillarResult from a resolved tree leaf.

        Override this to add custom post-processing (e.g., enriching
        with ontology data, computing scores, etc.).
        """
        return PillarResult(
            pillar_id=self.pillar_id,
            strategy=leaf.get("strategy", "Unknown"),
            tier=leaf.get("_leaf_id", "unknown"),
            reasoning=leaf.get("reasoning", ""),
            details={
                k: v
                for k, v in leaf.items()
                if k not in ("strategy", "reasoning", "_leaf_id")
            },
        )
