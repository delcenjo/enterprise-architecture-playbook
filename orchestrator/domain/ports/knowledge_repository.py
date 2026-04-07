"""
Port: KnowledgeRepository — Interface for loading knowledge-base resources.

Decouples the domain from specific storage backends (JSON files, databases,
remote APIs, etc.).  Each plugin receives a scoped repository instance that
resolves resource names relative to its own knowledge directory.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class KnowledgeRepository(ABC):
    """Abstract contract for loading structured knowledge resources."""

    @abstractmethod
    def load(self, resource_name: str) -> Dict[str, Any]:
        """Load a named knowledge resource and return its content.

        Parameters
        ----------
        resource_name:
            Logical name of the resource (e.g. ``'decision_tree'``,
            ``'ontology'``, ``'cases'``, ``'tradeoff_matrix'``).
            The adapter resolves this to a concrete storage path.

        Returns
        -------
        dict
            Parsed content of the resource.

        Raises
        ------
        FileNotFoundError
            If the resource cannot be located.
        ValueError
            If the resource content is malformed.
        """
        ...

    @abstractmethod
    def exists(self, resource_name: str) -> bool:
        """Check whether a named resource exists without loading it."""
        ...
