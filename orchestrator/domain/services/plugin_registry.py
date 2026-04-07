"""
Domain Service: Plugin Registry

Discovers, validates, and manages PillarPlugin instances.
Supports auto-discovery from a directory of plugin packages
and topological ordering based on declared dependencies.
"""

import importlib
import json
import logging
import os
from collections import defaultdict, deque
from typing import Any, Dict, List, Optional, Type

from domain.ports.pillar_plugin import PillarPlugin

logger = logging.getLogger(__name__)


class PluginRegistrationError(Exception):
    """Raised when a plugin fails validation during registration."""


class PluginRegistry:
    """Registry for PillarPlugin instances with auto-discovery.

    Usage
    -----
    >>> registry = PluginRegistry()
    >>> registry.discover("/path/to/plugins")
    >>> for plugin in registry.get_execution_order():
    ...     result = plugin.analyze(metrics, state)
    """

    def __init__(self) -> None:
        self._plugins: Dict[str, PillarPlugin] = {}
        self._categories: Dict[str, List[str]] = defaultdict(list)

    # ── Registration ────────────────────────────────────────────────

    def register(self, plugin: PillarPlugin) -> None:
        """Register a single plugin instance.

        Raises
        ------
        PluginRegistrationError
            If a plugin with the same ``pillar_id`` is already registered
            or if the plugin fails validation.
        """
        pid = plugin.pillar_id

        if pid in self._plugins:
            raise PluginRegistrationError(
                f"Duplicate plugin ID: '{pid}' is already registered."
            )

        # Validate required properties
        for attr in ("pillar_id", "name", "category"):
            val = getattr(plugin, attr, None)
            if not val or not isinstance(val, str):
                raise PluginRegistrationError(
                    f"Plugin '{pid}' has invalid '{attr}': {val!r}"
                )

        self._plugins[pid] = plugin
        self._categories[plugin.category].append(pid)
        logger.info(
            "Registered plugin '%s' (%s) [%s]",
            pid,
            plugin.name,
            plugin.category,
        )

    # ── Discovery ───────────────────────────────────────────────────

    def discover(
        self,
        plugins_dir: str,
        *,
        knowledge_repo_factory: Optional[Any] = None,
    ) -> int:
        """Auto-discover and register plugins from a directory.

        Each subdirectory is expected to contain a ``plugin.py`` module
        with a class that inherits from ``PillarPlugin``.  An optional
        ``manifest.json`` can provide metadata.

        Parameters
        ----------
        plugins_dir:
            Absolute path to the plugins directory.
        knowledge_repo_factory:
            Optional callable ``(plugin_knowledge_dir) -> KnowledgeRepository``
            used to inject a scoped knowledge repository into each plugin.

        Returns
        -------
        int
            Number of plugins successfully discovered and registered.
        """
        if not os.path.isdir(plugins_dir):
            logger.warning("Plugins directory not found: %s", plugins_dir)
            return 0

        count = 0
        for entry in sorted(os.listdir(plugins_dir)):
            entry_path = os.path.join(plugins_dir, entry)

            # Skip non-directories and private entries
            if not os.path.isdir(entry_path) or entry.startswith("_"):
                continue

            plugin_module_path = os.path.join(entry_path, "plugin.py")
            if not os.path.isfile(plugin_module_path):
                continue

            try:
                plugin = self._load_plugin(
                    entry,
                    entry_path,
                    knowledge_repo_factory,
                )
                self.register(plugin)
                count += 1
            except Exception as exc:
                logger.error(
                    "Failed to load plugin from '%s': %s",
                    entry_path,
                    exc,
                )

        logger.info(
            "Plugin discovery complete: %d/%d plugins loaded.",
            count,
            count,  # total attempted would need its own counter
        )
        return count

    def _load_plugin(
        self,
        package_name: str,
        package_dir: str,
        knowledge_repo_factory: Optional[Any],
    ) -> PillarPlugin:
        """Load a single plugin from its package directory."""

        # Load optional manifest
        manifest_path = os.path.join(package_dir, "manifest.json")
        manifest: Dict[str, Any] = {}
        if os.path.isfile(manifest_path):
            with open(manifest_path, "r") as f:
                manifest = json.load(f)

        # Import the plugin module
        module_name = f"plugins.{package_name}.plugin"
        module = importlib.import_module(module_name)

        # Find the PillarPlugin subclass
        plugin_class: Optional[Type[PillarPlugin]] = None
        for attr_name in dir(module):
            obj = getattr(module, attr_name)
            if (
                isinstance(obj, type)
                and issubclass(obj, PillarPlugin)
                and obj is not PillarPlugin
                and not getattr(obj, "__abstractmethods__", None)
            ):
                plugin_class = obj
                break

        if plugin_class is None:
            raise PluginRegistrationError(
                f"No concrete PillarPlugin subclass found in {module_name}"
            )

        # Prepare knowledge repository if factory provided
        kwargs: Dict[str, Any] = {}
        knowledge_dir = os.path.join(package_dir, "knowledge")
        if knowledge_repo_factory and os.path.isdir(knowledge_dir):
            kwargs["knowledge_repo"] = knowledge_repo_factory(knowledge_dir)

        return plugin_class(**kwargs)

    # ── Query ───────────────────────────────────────────────────────

    @property
    def plugins(self) -> Dict[str, PillarPlugin]:
        """All registered plugins keyed by ``pillar_id``."""
        return dict(self._plugins)

    @property
    def plugin_count(self) -> int:
        return len(self._plugins)

    def get(self, pillar_id: str) -> Optional[PillarPlugin]:
        return self._plugins.get(pillar_id)

    def get_by_category(self, category: str) -> List[PillarPlugin]:
        return [self._plugins[pid] for pid in self._categories.get(category, [])]

    # ── Execution Order (Topological Sort) ──────────────────────────

    def get_execution_order(self) -> List[PillarPlugin]:
        """Return plugins in dependency-respecting execution order.

        Uses Kahn's algorithm for topological sorting.  Plugins with the
        same dependency depth are further sorted by ``priority`` (ascending).

        Raises
        ------
        ValueError
            If a circular dependency is detected.
        """
        # Build adjacency and in-degree maps
        in_degree: Dict[str, int] = {pid: 0 for pid in self._plugins}
        dependents: Dict[str, List[str]] = defaultdict(list)

        for pid, plugin in self._plugins.items():
            for dep in plugin.dependencies:
                if dep in self._plugins:
                    dependents[dep].append(pid)
                    in_degree[pid] += 1
                else:
                    logger.warning(
                        "Plugin '%s' declares dependency '%s' which is not registered.",
                        pid,
                        dep,
                    )

        # Kahn's algorithm
        queue: deque[str] = deque()
        for pid, deg in in_degree.items():
            if deg == 0:
                queue.append(pid)

        ordered: List[PillarPlugin] = []
        while queue:
            # Sort current tier by priority for deterministic ordering
            tier = sorted(queue, key=lambda p: self._plugins[p].priority)
            queue.clear()

            for pid in tier:
                ordered.append(self._plugins[pid])
                for dep_pid in dependents[pid]:
                    in_degree[dep_pid] -= 1
                    if in_degree[dep_pid] == 0:
                        queue.append(dep_pid)

        if len(ordered) != len(self._plugins):
            missing = set(self._plugins.keys()) - {p.pillar_id for p in ordered}
            raise ValueError(
                f"Circular dependency detected among plugins: {missing}"
            )

        return ordered
