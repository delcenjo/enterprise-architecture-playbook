"""
Advanced LTV & Revenue Dynamics Engine - Verification Suite
Tests NRR calculation, dynamic LTV, churn stage detection,
expansion model routing, and severity-based recommendations.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from global_state import GlobalState

def setup_state(concurrent_users=500, annual_revenue=1000000, monthly_burn=50000,
                cac=0, churn_pct=5.0, gross_margin_pct=70.0, company_type="Enterprise",
                arch_type="Monolith", objectives=None, onboarding_maturity="Structured"):
    """Helper to create full state for LTV dynamics testing."""
    state = GlobalState()
    state.traffic_profile.concurrent_users = concurrent_users
    state.onboarding_profile.onboarding_maturity = onboarding_maturity
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
        },
        "current_architecture": {
            "architecture_type": arch_type
        },
        "user_objectives": {
            "strategic_goals": objectives or []
        }
    }
    return state

def test_elite_nrr_usage_based():
    """
    Test 1: Microservices architecture with usage-based expansion → NRR > 130% → Elite
    """
    print("\nTest 1: Elite NRR with Usage-Based Expansion")
    state = setup_state(
        concurrent_users=200,
        annual_revenue=6000000,
        cac=4000,
        churn_pct=1.5,
        gross_margin_pct=85.0,
        arch_type="Microservices",
        objectives=["Scale API consumption globally"]
    )

    from layers.core_engine import CoreEngine
    engine = CoreEngine(state)
    # Must run V66 first (dependency)
    engine._recommend_unit_economics_strategy({})
    result = engine._recommend_ltv_dynamics_strategy({})

    calcs = result["calculations"]
    print(f"  NRR Annual: {calcs['nrr_annual_pct']}%")
    print(f"  Expansion Model: {calcs['expansion_model']}")
    print(f"  Static LTV: €{calcs['static_ltv_eur']}")
    print(f"  Dynamic LTV: €{calcs['dynamic_ltv_eur']}")
    print(f"  LTV Multiplier: {calcs['ltv_multiplier']}x")
    print(f"  Cohort Health: {calcs['cohort_health']}")
    print(f"  Strategy: {result['strategy']}")

    assert calcs["expansion_model"] == "usage_based", f"Expected usage_based, got {calcs['expansion_model']}"
    assert calcs["dynamic_ltv_eur"] > calcs["static_ltv_eur"], "Dynamic LTV should exceed static LTV with expansion"
    assert "Elite" in result["strategy"] or "Scale" in result["strategy"], f"Expected elite strategy, got {result['strategy']}"
    print("  PASSED")

def test_dying_nrr_high_churn():
    """
    Test 2: High churn, no expansion → NRR < 90% → Revenue Contraction Crisis
    """
    print("\nTest 2: Dying NRR (High Churn, No Expansion)")
    state = setup_state(
        concurrent_users=100,
        annual_revenue=1200000,
        cac=2000,
        churn_pct=8.0,
        gross_margin_pct=70.0,
        arch_type="Monolith",
        onboarding_maturity="Ad-hoc"
    )

    from layers.core_engine import CoreEngine
    engine = CoreEngine(state)
    engine._recommend_unit_economics_strategy({})
    result = engine._recommend_ltv_dynamics_strategy({})

    calcs = result["calculations"]
    print(f"  NRR Annual: {calcs['nrr_annual_pct']}%")
    print(f"  Churn Stage: {calcs['churn_stage']}")
    print(f"  Cohort Health: {calcs['cohort_health']}")
    print(f"  Strategy: {result['strategy']}")
    print(f"  Severity: {result['severity']}")

    assert calcs["nrr_annual_pct"] < 90, f"Expected NRR < 90%, got {calcs['nrr_annual_pct']}%"
    assert calcs["cohort_health"] == "degrading", f"Expected degrading, got {calcs['cohort_health']}"
    assert result["severity"] == "critical", f"Expected critical severity, got {result['severity']}"
    print("  PASSED")

def test_mediocre_nrr_early_churn():
    """
    Test 3: Mediocre NRR with early churn (poor onboarding) → Onboarding fix
    """
    print("\nTest 3: Mediocre NRR — Early Churn (Onboarding Problem)")
    state = setup_state(
        concurrent_users=300,
        annual_revenue=3600000,
        cac=3000,
        churn_pct=6.0,
        gross_margin_pct=75.0,
        arch_type="Monolith",
        onboarding_maturity="Ad-hoc"
    )

    from layers.core_engine import CoreEngine
    engine = CoreEngine(state)
    engine._recommend_unit_economics_strategy({})
    result = engine._recommend_ltv_dynamics_strategy({})

    calcs = result["calculations"]
    print(f"  NRR Annual: {calcs['nrr_annual_pct']}%")
    print(f"  Churn Stage: {calcs['churn_stage']}")
    print(f"  Strategy: {result['strategy']}")

    assert calcs["churn_stage"] == "early", f"Expected early churn stage, got {calcs['churn_stage']}"
    assert "Onboarding" in result["strategy"] or "Early" in result["strategy"], f"Expected onboarding fix, got {result['strategy']}"
    print("  PASSED")

def test_good_nrr_seat_expansion():
    """
    Test 4: Good NRR with seat-based model → Optimize adoption
    """
    print("\nTest 4: Good NRR — Seat-Based Expansion")
    state = setup_state(
        concurrent_users=800,
        annual_revenue=4800000,
        cac=5000,
        churn_pct=2.5,
        gross_margin_pct=80.0,
        arch_type="Microservices",
        objectives=["Expand team collaboration features"]
    )

    from layers.core_engine import CoreEngine
    engine = CoreEngine(state)
    engine._recommend_unit_economics_strategy({})
    result = engine._recommend_ltv_dynamics_strategy({})

    calcs = result["calculations"]
    print(f"  NRR Annual: {calcs['nrr_annual_pct']}%")
    print(f"  Expansion Model: {calcs['expansion_model']}")
    print(f"  Dynamic LTV: €{calcs['dynamic_ltv_eur']}")
    print(f"  Strategy: {result['strategy']}")
    print(f"  Architecture Impact: {result.get('architecture_impact', 'N/A')}")

    assert calcs["expansion_model"] == "seat_based", f"Expected seat_based, got {calcs['expansion_model']}"
    assert "architecture_impact" in result, "Missing architecture_impact field"
    print("  PASSED")


if __name__ == "__main__":
    print("Advanced LTV & Revenue Dynamics Engine - Verification")

    test_elite_nrr_usage_based()
    test_dying_nrr_high_churn()
    test_mediocre_nrr_early_churn()
    test_good_nrr_seat_expansion()

    print("\nALL LTV DYNAMICS TESTS PASSED")
