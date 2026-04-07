"""
Adapter: JsonFileRepository — Loads knowledge resources from JSON files.

This is the primary adapter for the KnowledgeRepository port.
Each plugin receives a scoped instance pointing to its own ``knowledge/``
directory so that ``load("decision_tree")`` resolves to
``<plugin_dir>/knowledge/decision_tree.json``.
"""

import json
import logging
import os
from functools import lru_cache
from typing import Any, Dict

from domain.ports.knowledge_repository import KnowledgeRepository

logger = logging.getLogger(__name__)


class JsonFileRepository(KnowledgeRepository):
    """Concrete KnowledgeRepository that reads ``.json`` files from a directory.

    Parameters
    ----------
    base_dir:
        Absolute path to the directory containing JSON knowledge files.
    cache_enabled:
        If ``True`` (default), parsed JSON is cached in memory after
        the first load.  Suitable for read-heavy knowledge bases that
        don't change at runtime.
    """

    def __init__(self, base_dir: str, *, cache_enabled: bool = True) -> None:
        if not os.path.isdir(base_dir):
            raise FileNotFoundError(
                f"Knowledge directory not found: {base_dir}"
            )
        self._base_dir = base_dir
        self._cache_enabled = cache_enabled
        self._cache: Dict[str, Dict[str, Any]] = {}

    # ── KnowledgeRepository interface ──────────────────────────────

    def load(self, resource_name: str) -> Dict[str, Any]:
        """Load a JSON resource by its logical name.

        The ``resource_name`` is resolved to ``<base_dir>/<resource_name>.json``.
        """
        if self._cache_enabled and resource_name in self._cache:
            return self._cache[resource_name]

        file_path = self._resolve_path(resource_name)
        if not os.path.isfile(file_path):
            raise FileNotFoundError(
                f"Knowledge resource '{resource_name}' not found at {file_path}"
            )

        logger.debug("Loading knowledge resource: %s", file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if self._cache_enabled:
            self._cache[resource_name] = data

        return data

    def exists(self, resource_name: str) -> bool:
        """Check if a resource file exists."""
        return os.path.isfile(self._resolve_path(resource_name))

    # ── Helpers ─────────────────────────────────────────────────────

    def _resolve_path(self, resource_name: str) -> str:
        """Resolve a logical resource name to a filesystem path."""
        # Support both "decision_tree" and "decision_tree.json"
        if not resource_name.endswith(".json"):
            resource_name += ".json"
        return os.path.join(self._base_dir, resource_name)

    def clear_cache(self) -> None:
        """Clear the in-memory cache."""
        self._cache.clear()

    @property
    def base_dir(self) -> str:
        return self._base_dir

    def __repr__(self) -> str:
        cached = len(self._cache)
        return f"JsonFileRepository(base_dir='{self._base_dir}', cached={cached})"
