"""Advanced LTV & Revenue Dynamics Plugin."""
from typing import Any, Dict
from domain.ports.pillar_plugin import PillarPlugin, PillarResult
from domain.ports.knowledge_repository import KnowledgeRepository


class LTVDynamicsPlugin(PillarPlugin):
    """Non-standard: performs dynamic LTV modeling with cohort decay."""
    pillar_id = "ltv_dynamics"
    name = "Advanced LTV & Revenue Dynamics"
    category = "financial"
    dependencies = ["unit_economics"]

    def __init__(self, knowledge_repo: KnowledgeRepository = None, **kwargs):
        self._repo = knowledge_repo

    def analyze(self, metrics: Dict[str, Any], state: Any) -> PillarResult:
        tree = self._repo.load("decision_tree") if self._repo else {"nodes": []}

        ue = getattr(state, "unit_economics_profile", None)
        churn_pct = getattr(ue, "monthly_churn_pct", 5.0) if ue else 5.0
        monthly_arpu = getattr(ue, "monthly_arpu", 100.0) if ue else 100.0
        gross_margin_pct = getattr(ue, "gross_margin_pct", 70.0) if ue else 70.0
        static_ltv = getattr(ue, "ltv", 0) if ue else 0

        raw = getattr(state, "raw_input", {})
        objectives = raw.get("user_objectives", {}).get("strategic_goals", [])
        obj_text = " ".join(objectives).lower() if objectives else ""

        if "usage" in obj_text or "api" in obj_text:
            expansion_model, expansion_pct = "usage_based", 5.0
        elif "seats" in obj_text or "team" in obj_text:
            expansion_model, expansion_pct = "seat_based", 3.0
        elif "upgrade" in obj_text or "enterprise" in obj_text:
            expansion_model, expansion_pct = "tiered", 2.0
        else:
            expansion_model, expansion_pct = "none", 0.0

        contraction_pct = churn_pct
        nrr_monthly = 100.0 - contraction_pct + expansion_pct
        nrr_annual = ((nrr_monthly / 100.0) ** 12) * 100.0

        ob = getattr(state, "onboarding_profile", None)
        ob_maturity = getattr(ob, "onboarding_maturity", "Ad-hoc") if ob else "Ad-hoc"
        if ob_maturity == "Ad-hoc" and churn_pct > 5: churn_stage = "early"
        elif churn_pct > 3 and expansion_pct < 1: churn_stage = "mid"
        elif churn_pct <= 3 and expansion_pct < 1: churn_stage = "late"
        else: churn_stage = "mid"

        gm = monthly_arpu * (gross_margin_pct / 100.0)
        dynamic_ltv, retention, revenue = 0.0, 1.0, gm
        for month in range(1, 61):
            period_churn = (churn_pct * 1.5 / 100.0) if month <= 3 else (churn_pct * 0.8 / 100.0)
            retention *= (1.0 - period_churn)
            if month > 6: revenue *= (1.0 + expansion_pct / 100.0)
            dynamic_ltv += revenue * retention

        cohort_health = "stabilizing" if nrr_annual > 110 else "flat" if nrr_annual >= 95 else "degrading"

        ldp = getattr(state, "ltv_dynamics_profile", None)
        if ldp:
            ldp.nrr_pct = round(nrr_annual, 1)
            ldp.expansion_revenue_pct = expansion_pct
            ldp.contraction_revenue_pct = contraction_pct
            ldp.expansion_model = expansion_model
            ldp.churn_stage = churn_stage
            ldp.cohort_health = cohort_health
            ldp.dynamic_ltv = round(dynamic_ltv, 2)

        if nrr_annual < 90: nrr_bucket = "dying"
        elif nrr_annual < 100: nrr_bucket = "mediocre"
        elif nrr_annual < 115: nrr_bucket = "good"
        elif nrr_annual <= 130: nrr_bucket = "excellent"
        else: nrr_bucket = "elite"

        root_node = next((n for n in tree.get("nodes", []) if n["id"] == "root"), None)
        target_id = root_node["branches"].get(nrr_bucket) if root_node else "value_delivery_gap"

        if target_id == "check_churn_stage":
            cn = next((n for n in tree.get("nodes", []) if n["id"] == "check_churn_stage"), None)
            if cn: target_id = cn["branches"].get(churn_stage, "value_delivery_gap")

        if target_id == "check_expansion_model":
            en = next((n for n in tree.get("nodes", []) if n["id"] == "check_expansion_model"), None)
            if en: target_id = en["branches"].get(expansion_model, "implement_expansion_strategy")

        rec_node = next((n for n in tree.get("nodes", []) if n["id"] == target_id), None)
        strategy = rec_node["recommendation"] if rec_node else "Fallback"
        reasoning = rec_node["rationale"] if rec_node else "No matching node."

        ltv_mult = dynamic_ltv / max(static_ltv, 1.0) if static_ltv > 0 else 0

        return PillarResult(
            pillar_id=self.pillar_id,
            strategy=strategy,
            tier=target_id or "unknown",
            reasoning=reasoning,
            details={
                "severity": rec_node.get("severity", "unknown") if rec_node else "unknown",
                "calculations": {
                    "nrr_annual_pct": round(nrr_annual, 1),
                    "expansion_model": expansion_model,
                    "static_ltv_eur": round(static_ltv, 2),
                    "dynamic_ltv_eur": round(dynamic_ltv, 2),
                    "ltv_multiplier": round(ltv_mult, 2),
                    "churn_stage": churn_stage,
                    "cohort_health": cohort_health,
                },
            },
        )
