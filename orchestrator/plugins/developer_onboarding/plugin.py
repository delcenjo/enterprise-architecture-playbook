"""Developer Onboarding Plugin (V65)."""
from typing import Any, Dict
from domain.ports.pillar_plugin import PillarPlugin, PillarResult
from domain.ports.knowledge_repository import KnowledgeRepository


class DeveloperOnboardingPlugin(PillarPlugin):
    """Non-standard: uses direct routing + 30-day plan generation."""
    pillar_id = "developer_onboarding"
    name = "Developer Onboarding & Productivity"
    category = "organization"

    def __init__(self, knowledge_repo: KnowledgeRepository = None, **kwargs):
        self._repo = knowledge_repo

    def analyze(self, metrics: Dict[str, Any], state: Any) -> PillarResult:
        tree = self._repo.load("decision_tree") if self._repo else {"nodes": [], "leaves": {}}

        tsp = getattr(state, "team_structure_profile", None)
        devs = getattr(tsp, "total_developers", 5) if tsp else 5
        platform_maturity = getattr(tsp, "platform_maturity", "none") if tsp else "none"

        # Decision routing
        if devs > 40:
            if platform_maturity == "mature":
                node_id = "data_driven_onboarding"
                maturity = "Data-Driven"
                ttfc, ttfp = 2, 8
            else:
                node_id = "standard_enterprise_onboarding"
                maturity = "Structured"
                ttfc, ttfp = 3, 10
        elif devs >= 10:
            node_id = "standard_agile_onboarding"
            maturity = "Structured"
            ttfc, ttfp = 3, 10
        else:
            node_id = "basic_startup_onboarding"
            maturity = "Ad-hoc"
            ttfc, ttfp = 2, 7

        # Update state profile if available
        ob = getattr(state, "onboarding_profile", None)
        if ob:
            ob.onboarding_maturity = maturity
            ob.ttfc_target_days = ttfc
            ob.ttfp_target_days = ttfp

        # Fetch from tree
        nodes = tree.get("nodes", [])
        rec_node = next((n for n in nodes if n["id"] == node_id), None)

        thirty_day_plan = {
            "phase_0_pre_day1": {
                "name": "Pre-boarding Setup",
                "golden_rule": "New dev should run the system in < 1 hour",
                "requirements": ["Docker/DevContainer setup script", "Access provisioned", "Onboarding roadmap visible"]
            },
            "week_1_context": {"name": "Context + First Impact", "target_ttfc": f"{ttfc} days"},
            "week_2_deep_dive": {"name": "Deep Comprehension"},
            "week_3_guided_autonomy": {"name": "Guided Autonomy"},
            "week_4_simulated_seniority": {"name": "Simulated Seniority", "target_ttfp": f"{ttfp} days"},
        }

        strategy = rec_node["recommendation"] if rec_node else "Fallback"
        reasoning = rec_node["rationale"] if rec_node else "No matching onboarding node found."

        return PillarResult(
            pillar_id=self.pillar_id,
            strategy=strategy,
            tier=node_id,
            reasoning=reasoning,
            details={
                "maturity_level": maturity,
                "thirty_day_plan": thirty_day_plan,
                "key_metrics": {"ttfc_target": f"< {ttfc} days", "ttfp_target": f"< {ttfp} days"},
            },
        )
