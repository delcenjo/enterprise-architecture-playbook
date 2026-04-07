"""
Domain Service: Pipeline Orchestrator

The main coordinator for the architectural analysis process.
Replaces the `IntelligentDossierForge` and wraps the legacy `CoreEngine`
to enable the "Hybrid Migration Strategy".

It runs auto-discovered plugins first, injects their results into
the state, and then invokes the legacy engine for pillars that haven't
been migrated yet.
"""

import logging
from typing import Any, Dict

from adapters.knowledge.json_file_repository import JsonFileRepository
from domain.services.plugin_registry import PluginRegistry
from layers.core_engine import CoreEngine

logger = logging.getLogger(__name__)


class PipelineOrchestrator:
    """Orchestrates the execution of architectural analysis plugins."""

    def __init__(self, plugins_dir: str):
        self.registry = PluginRegistry()
        
        # Factory for KnowledgeRepository isolated per plugin
        def repo_factory(knowledge_dir: str) -> JsonFileRepository:
            return JsonFileRepository(knowledge_dir, cache_enabled=True)

        # Discover plugins
        self.registry.discover(plugins_dir, knowledge_repo_factory=repo_factory)
        
        self.plugins_to_run = self.registry.get_execution_order()

    def run_layer_2(self, state: Any, metrics: Dict[str, Any], adapted_spec: Dict[str, Any]) -> None:
        """Run the architectural analysis (Layer 2).
        
        In hybrid mode, we run plugins first. For any plugin that runs,
        we inject its result into the `adapted_spec` using the pillar_id or
        the expected legacy key, so the legacy code doesn't override it.
        """
        logger.info("🚀 Running Hybrid Architecture Layer (Plugins + Legacy)...")
        
        # Legacy key mapping: plugin pillar_id -> adapted_spec key
        legacy_key_map = {
            "sre_reliability": "reliability",
            "distributed_tracing": "tracing",
            "chaos_engineering": "chaos",
            "deployment_strategy": "deployment",
            "gitops": "gitops",
            "supply_chain_security": "supply_chain",
            "infrastructure_as_code": "iac",
            "load_testing": "performance",
            "profiling": "profiling",
            "db_optimization": "db_optimization",
            "frontend_performance": "frontend_perf",
            "tech_debt": "tech_debt",
            "code_review": "code_review",
            "fitness_functions": "aff",
            "scalability": "scalability",
            "tpm_prioritization": "tpm",
            "okr_metrics": "okrs",
            "tradeoff_analysis": "tradeoff_analysis",
            "platform_engineering": "platform_engineering",
            "senior_evaluation": "senior_evaluation",
            "cultural_fit": "cultural_fit",
            "team_structure": "team_structure",
            "developer_onboarding": "onboarding",
            "unit_economics": "unit_economics",
            "ltv_dynamics": "ltv_dynamics",
            "observability": "observability",
        }
        
        for plugin in self.plugins_to_run:
            logger.info(f"🔌 Running plugin: {plugin.pillar_id} ({plugin.name})")
            try:
                result = plugin.analyze(metrics, state)
                
                # Store in state's pillar_results
                if hasattr(state, "pillar_results"):
                    state.pillar_results[plugin.pillar_id] = result
                
                # Build a legacy-compatible dict from PillarResult.
                # Legacy format: {"strategy": ..., "tier": ..., "pillars": [...], "reasoning": ...}
                # plus any plugin-specific keys from details.
                legacy_dict = dict(result.details)  # start with all details
                legacy_dict["strategy"] = result.strategy
                legacy_dict["tier"] = result.tier
                legacy_dict["reasoning"] = result.reasoning
                # Ensure 'pillars' exists (most legacy tests check it)
                if "pillars" not in legacy_dict:
                    legacy_dict["pillars"] = legacy_dict.get("pillars", [])
                
                legacy_key = legacy_key_map.get(plugin.pillar_id, plugin.pillar_id)
                adapted_spec[legacy_key] = legacy_dict
                    
            except Exception as e:
                logger.error(f"Plugin {plugin.pillar_id} failed: {e}", exc_info=True)

