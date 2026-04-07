"""Unit Economics & CAC Plugin (V66)."""
from typing import Any, Dict
from domain.ports.pillar_plugin import PillarPlugin, PillarResult
from domain.ports.knowledge_repository import KnowledgeRepository


class UnitEconomicsPlugin(PillarPlugin):
    """Non-standard: performs financial calculations + tree routing."""
    pillar_id = "unit_economics"
    name = "Unit Economics & CAC Analysis"
    category = "financial"
    dependencies = ["developer_onboarding"]

    def __init__(self, knowledge_repo: KnowledgeRepository = None, **kwargs):
        self._repo = knowledge_repo

    def analyze(self, metrics: Dict[str, Any], state: Any) -> PillarResult:
        tree = self._repo.load("decision_tree") if self._repo else {"nodes": []}

        financials = getattr(state, "raw_input", {}).get("financials", {})
        annual_revenue = float(financials.get("annual_revenue", 1000000))
        monthly_burn = float(financials.get("monthly_burn_rate", 50000))
        cac_input = float(financials.get("cac", 0))
        churn_pct = float(financials.get("churn_rate_pct", 5.0))
        gross_margin_pct = float(financials.get("gross_margin_pct", 70.0))

        tp = getattr(state, "traffic_profile", None)
        concurrent = getattr(tp, "concurrent_users", 10) if tp else 10
        mau = max(concurrent * 10, 100)
        monthly_arpu = (annual_revenue / 12.0) / max(mau, 1)

        cac = cac_input if cac_input > 0 else monthly_burn * 0.6
        gm_per_customer = monthly_arpu * (gross_margin_pct / 100.0)
        payback_months = cac / max(gm_per_customer, 1.0)
        monthly_churn = churn_pct / 100.0
        avg_lifetime = 1.0 / max(monthly_churn, 0.005)
        ltv = gm_per_customer * avg_lifetime
        ltv_cac_ratio = ltv / max(cac, 1.0)

        # Update state profile
        ue = getattr(state, "unit_economics_profile", None)
        if ue:
            ue.cac = round(cac, 2)
            ue.monthly_arpu = round(monthly_arpu, 2)
            ue.gross_margin_pct = gross_margin_pct
            ue.monthly_churn_pct = churn_pct
            ue.ltv = round(ltv, 2)
            ue.payback_months = round(payback_months, 1)
            ue.ltv_cac_ratio = round(ltv_cac_ratio, 2)

        # Route
        if ltv_cac_ratio < 1.0: ltv_bucket = "dead"
        elif ltv_cac_ratio < 3.0: ltv_bucket = "mediocre"
        elif ltv_cac_ratio <= 5.0: ltv_bucket = "healthy"
        else: ltv_bucket = "over_optimized"

        root_node = next((n for n in tree.get("nodes", []) if n["id"] == "root"), None)
        target_id = root_node["branches"].get(ltv_bucket) if root_node else "monitor_and_optimize"

        if target_id == "check_payback":
            if payback_months < 12: pb = "excellent"
            elif payback_months <= 18: pb = "acceptable"
            elif payback_months <= 24: pb = "dangerous"
            else: pb = "unsustainable"
            pb_node = next((n for n in tree.get("nodes", []) if n["id"] == "check_payback"), None)
            if pb_node:
                target_id = pb_node["branches"].get(pb, "monitor_and_optimize")

        rec_node = next((n for n in tree.get("nodes", []) if n["id"] == target_id), None)
        strategy = rec_node["recommendation"] if rec_node else "Fallback"
        reasoning = rec_node["rationale"] if rec_node else "No matching node."

        return PillarResult(
            pillar_id=self.pillar_id,
            strategy=strategy,
            tier=target_id or "unknown",
            reasoning=reasoning,
            details={
                "severity": rec_node.get("severity", "unknown") if rec_node else "unknown",
                "actions": rec_node.get("actions", []) if rec_node else [],
                "calculations": {
                    "cac_eur": round(cac, 2),
                    "monthly_arpu_eur": round(monthly_arpu, 2),
                    "payback_months": round(payback_months, 1),
                    "ltv_eur": round(ltv, 2),
                    "ltv_cac_ratio": round(ltv_cac_ratio, 2),
                },
            },
        )
