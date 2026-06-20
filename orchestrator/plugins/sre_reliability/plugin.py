"""
SRE & Reliability Engineering Plugin.

Replaces the legacy `_recommend_sre_reliability` method from `CoreEngine`.
"""

from typing import Any, Callable, Dict

from domain.ports.pillar_plugin import PillarResult
from plugins._base import BaseDecisionTreePlugin


class SREReliabilityPlugin(BaseDecisionTreePlugin):
    pillar_id = "sre_reliability"
    name = "SRE & Reliability Engineering"
    category = "operations"

    @property
    def default_leaf(self) -> str:
        return "leaf_basic_metrics"

    def build_question_map(
        self,
        metrics: Dict[str, Any],
        state: Any,
    ) -> Dict[str, Callable[[Dict[str, Any]], str]]:
        """Map decision tree questions to metric evaluations."""
        return {
            "root": lambda m: "start",
            "business_criticality_check": lambda m: "yes"
            if m.get("scaling_problem") or m.get("is_psd2_scope")
            else "no",
            "recommend_strict_slo": lambda m: "yes"
            if m.get("is_aml_scope") or m.get("is_bde_supervised")
            else "no",
            "recommend_moderate_slo": lambda m: "yes"
            if m.get("is_gdpr_critical")
            else "no",
        }

    def build_result(
        self,
        leaf: Dict[str, Any],
        ontology: Dict[str, Any],
        metrics: Dict[str, Any],
        state: Any,
    ) -> PillarResult:
        """Enrich the base result with ontology definitions for SLIs."""
        slis = []
        for sli_name in leaf.get("slis", []):
            if sli_name in ontology:
                slis.append(ontology[sli_name])

        return PillarResult(
            pillar_id=self.pillar_id,
            strategy=leaf.get("strategy", "Unknown"),
            tier=leaf.get("_leaf_id", "unknown"),
            reasoning=leaf.get("reasoning", ""),
            details={
                "slo_target": leaf.get("slo_target", 99.0),
                "sla_active": leaf.get("sla_active", False),
                "features": leaf.get("features", []),
                "slis": slis,
                "reliability_tier": leaf.get("_leaf_id"),
            },
        )
