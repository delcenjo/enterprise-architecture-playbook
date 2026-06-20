"""
V66: Unit Economics & CAC Engine - Verification Suite
Tests the deterministic calculation and routing of CAC, Payback Period,
LTV/CAC ratio, and severity-based recommendations.
"""
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from global_state import GlobalState

def setup_state(concurrent_users=500, annual_revenue=1000000, monthly_burn=50000,
                cac=0, churn_pct=5.0, gross_margin_pct=70.0, company_type="Enterprise"):
    """Helper to create a GlobalState with specific financial parameters."""
    state = GlobalState()
    state.traffic_profile.concurrent_users = concurrent_users
    state.raw_input = {
        "financials": {
            "annual_revenue": annual_revenue,
            "monthly_burn_rate": monthly_burn,
            "cac": cac,
            "churn_rate_pct": churn_pct,
            "gross_margin_pct": gross_margin_pct
        },
        "project_context": {
            "company_type": company_type,
            "industry": "SaaS"
        }
    }
    return state

def test_healthy_unit_economics():
    """
    Test 1: Enterprise with high ARPU, low churn → Healthy / Scale Confidently
    """
    print("\nTest 1: Healthy Unit Economics (Enterprise, high ARPU)")
    state = setup_state(
        concurrent_users=100,
        annual_revenue=6000000,  # 6M/year → 500k/month → 500€ ARPU for 1000 MAU
        cac=4000,
        churn_pct=2.0,
        gross_margin_pct=80.0,
        company_type="Enterprise"
    )
    
    from layers.core_engine import CoreEngine
    engine = CoreEngine(state)
    result = engine._recommend_unit_economics_strategy({})
    
    calcs = result["calculations"]
    print(f"  CAC: €{calcs['cac_eur']}")
    print(f"  ARPU: €{calcs['monthly_arpu_eur']}/month")
    print(f"  Gross Margin/Customer: €{calcs['gross_margin_per_customer_eur']}/month")
    print(f"  Payback: {calcs['payback_months']} months")
    print(f"  LTV: €{calcs['ltv_eur']}")
    print(f"  LTV/CAC: {calcs['ltv_cac_ratio']}x")
    print(f"  Strategy: {result['strategy']}")
    print(f"  Severity: {result['severity']}")
    
    assert calcs["ltv_cac_ratio"] >= 3.0, f"Expected LTV/CAC >= 3, got {calcs['ltv_cac_ratio']}"
    assert "healthy" in result["severity"] or "over_optimized" in result.get("severity", ""), "Expected healthy/over_optimized severity"
    print("  PASSED")

def test_dead_unit_economics():
    """
    Test 2: SMB with high churn → LTV/CAC < 1 → Dead
    """
    print("\nTest 2: Dead Unit Economics (SMB, brutal churn)")
    state = setup_state(
        concurrent_users=1000,
        annual_revenue=600000,  # 50k/month → 5€ ARPU for 10k MAU
        cac=800,
        churn_pct=8.0,
        gross_margin_pct=75.0,
        company_type="Startup"
    )
    
    from layers.core_engine import CoreEngine
    engine = CoreEngine(state)
    result = engine._recommend_unit_economics_strategy({})
    
    calcs = result["calculations"]
    print(f"  CAC: €{calcs['cac_eur']}")
    print(f"  ARPU: €{calcs['monthly_arpu_eur']}/month")
    print(f"  Payback: {calcs['payback_months']} months")
    print(f"  LTV: €{calcs['ltv_eur']}")
    print(f"  LTV/CAC: {calcs['ltv_cac_ratio']}x")
    print(f"  Strategy: {result['strategy']}")
    print(f"  Severity: {result['severity']}")
    
    assert result["severity"] == "critical", f"Expected critical severity, got {result['severity']}"
    assert "Crisis" in result["strategy"] or "Survival" in result["strategy"], "Expected crisis/survival strategy"
    print("  PASSED")

def test_mediocre_with_dangerous_payback():
    """
    Test 3: Mid-market with mediocre LTV/CAC and long payback → Restructure
    """
    print("\nTest 3: Mediocre LTV/CAC with Dangerous Payback (20 months)")
    state = setup_state(
        concurrent_users=200,
        annual_revenue=2400000,
        cac=8000,
        churn_pct=3.0,
        gross_margin_pct=70.0,
        company_type="Scale-up"
    )
    
    from layers.core_engine import CoreEngine
    engine = CoreEngine(state)
    result = engine._recommend_unit_economics_strategy({})
    
    calcs = result["calculations"]
    print(f"  CAC: €{calcs['cac_eur']}")
    print(f"  ARPU: €{calcs['monthly_arpu_eur']}/month")
    print(f"  Payback: {calcs['payback_months']} months")
    print(f"  LTV: €{calcs['ltv_eur']}")
    print(f"  LTV/CAC: {calcs['ltv_cac_ratio']}x")
    print(f"  Strategy: {result['strategy']}")
    print(f"  Severity: {result['severity']}")
    
    assert result["severity"] in ["moderate", "high", "critical"], f"Expected moderate/high/critical, got {result['severity']}"
    assert "brutal_truth" in result, "Missing brutal truth"
    print("  PASSED")

def test_over_optimized_growth_warning():
    """
    Test 4: Excellent economics but LTV/CAC > 5 → Under-investing in growth
    """
    print("\nTest 4: Over-Optimized (LTV/CAC > 5, growth warning)")
    state = setup_state(
        concurrent_users=50,
        annual_revenue=3000000,  # high ARPU per user
        cac=2000,
        churn_pct=1.0,
        gross_margin_pct=85.0,
        company_type="Enterprise"
    )
    
    from layers.core_engine import CoreEngine
    engine = CoreEngine(state)
    result = engine._recommend_unit_economics_strategy({})
    
    calcs = result["calculations"]
    print(f"  CAC: €{calcs['cac_eur']}")
    print(f"  ARPU: €{calcs['monthly_arpu_eur']}/month")
    print(f"  LTV: €{calcs['ltv_eur']}")
    print(f"  LTV/CAC: {calcs['ltv_cac_ratio']}x")
    print(f"  Strategy: {result['strategy']}")
    print(f"  Severity: {result['severity']}")
    
    assert calcs["ltv_cac_ratio"] > 5.0, f"Expected LTV/CAC > 5, got {calcs['ltv_cac_ratio']}"
    assert result["severity"] == "warning", f"Expected warning severity, got {result['severity']}"
    assert "Under-Investment" in result["strategy"], "Expected growth under-investment warning"
    print("  PASSED")


if __name__ == "__main__":
    print("=" * 70)
    print("V66: Unit Economics & CAC Engine - Verification")
    print("=" * 70)
    
    test_healthy_unit_economics()
    test_dead_unit_economics()
    test_mediocre_with_dangerous_payback()
    test_over_optimized_growth_warning()
    
    print("\n" + "=" * 70)
    print("ALL V66 UNIT ECONOMICS TESTS PASSED")
    print("=" * 70)
