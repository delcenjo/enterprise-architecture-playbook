"""
Developer Onboarding & Productivity Engine - Verification Suite
Tests the deterministic routing of onboarding strategies based on
team size, platform maturity, and deployment frequency.
"""
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from global_state import GlobalState

def setup_state(total_devs, platform_maturity="none", reg_level="low"):
    """Helper to create a GlobalState with specific team parameters."""
    state = GlobalState()
    state.team_structure_profile.total_developers = total_devs
    state.team_structure_profile.platform_maturity = platform_maturity
    state.team_structure_profile.regulatory_level = reg_level
    return state

def test_startup_lean_onboarding():
    """Startup < 10 devs → Lean Developer Immersion. Ad-hoc maturity, TTFC < 2 days."""
    print("\nTest: Startup Lean Onboarding (< 10 devs)")
    state = setup_state(total_devs=6)
    
    from layers.core_engine import CoreEngine
    engine = CoreEngine(state)
    result = engine._recommend_onboarding_strategy({})
    
    assert result["strategy"] == "Lean Developer Immersion", f"Expected 'Lean Developer Immersion', got '{result['strategy']}'"
    assert result["maturity_level"] == "Ad-hoc", f"Expected 'Ad-hoc', got '{result['maturity_level']}'"
    assert state.onboarding_profile.ttfc_target_days == 2, f"Expected TTFC 2, got {state.onboarding_profile.ttfc_target_days}"
    assert state.onboarding_profile.ttfp_target_days == 7, f"Expected TTFP 7, got {state.onboarding_profile.ttfp_target_days}"
    assert "thirty_day_plan" in result, "Missing 30-day plan"
    assert "buddy_system" in result, "Missing buddy system spec"
    assert "anti_patterns" in result, "Missing anti-patterns list"
    
    print(f"  Strategy: {result['strategy']}")
    print(f"  Maturity: {result['maturity_level']}")
    print(f"  TTFC Target: {state.onboarding_profile.ttfc_target_days} days")
    print(f"  TTFP Target: {state.onboarding_profile.ttfp_target_days} days")
    print(f"  30-Day Plan: {len(result['thirty_day_plan'])} phases")
    print("  PASSED")

def test_agile_structured_onboarding():
    """Scale-up 10-40 devs → Structured 30-Day Mentorship. TTFC < 3 days, formalized buddy."""
    print("\nTest: Agile Scale-up Onboarding (25 devs)")
    state = setup_state(total_devs=25)
    
    from layers.core_engine import CoreEngine
    engine = CoreEngine(state)
    result = engine._recommend_onboarding_strategy({})
    
    assert result["strategy"] == "Structured 30-Day Mentorship", f"Expected 'Structured 30-Day Mentorship', got '{result['strategy']}'"
    assert result["maturity_level"] == "Structured", f"Expected 'Structured', got '{result['maturity_level']}'"
    assert state.onboarding_profile.ttfc_target_days == 3
    assert state.onboarding_profile.ttfp_target_days == 10
    assert result["buddy_system"]["sessions_per_week"] == 2, "Buddy system must have 2 sessions/week"
    assert "Can deploy without supervision" in result["thirty_day_plan"]["week_4_simulated_seniority"]["success_criteria"]
    
    print(f"  Strategy: {result['strategy']}")
    print(f"  Maturity: {result['maturity_level']}")
    print(f"  Buddy Sessions/Week: {result['buddy_system']['sessions_per_week']}")
    print(f"  Week 4 Success Criteria: {result['thirty_day_plan']['week_4_simulated_seniority']['success_criteria']}")
    print("  PASSED")

def test_enterprise_no_platform_onboarding():
    """Enterprise > 40 devs, no platform team → Standardized Enterprise Onboarding. ADR mandates."""
    print("\nTest: Enterprise Onboarding WITHOUT Platform Team (60 devs)")
    state = setup_state(total_devs=60, platform_maturity="none")
    
    from layers.core_engine import CoreEngine
    engine = CoreEngine(state)
    result = engine._recommend_onboarding_strategy({})
    
    assert result["strategy"] == "Standardized Enterprise Onboarding", f"Expected 'Standardized Enterprise Onboarding', got '{result['strategy']}'"
    assert result["maturity_level"] == "Structured"
    assert "ADRs (Architecture Decision Records)" in result["infrastructure_prerequisites"]["documentation"]
    assert "Outdated documentation" in result["anti_patterns"]
    
    print(f"  Strategy: {result['strategy']}")
    print(f"  Maturity: {result['maturity_level']}")
    print(f"  ADR Prerequisite: Present")
    print(f"  Anti-patterns: {len(result['anti_patterns'])} detected")
    print("  PASSED")

def test_data_driven_platform_onboarding():
    """Mature Platform > 40 devs → Data-Driven Platform Onboarding. TTFC automated tracking."""
    print("\nTest: Data-Driven Platform Onboarding (80 devs, mature platform)")
    state = setup_state(total_devs=80, platform_maturity="mature")
    
    from layers.core_engine import CoreEngine
    engine = CoreEngine(state)
    result = engine._recommend_onboarding_strategy({})
    
    assert result["strategy"] == "Data-Driven Platform Onboarding", f"Expected 'Data-Driven Platform Onboarding', got '{result['strategy']}'"
    assert result["maturity_level"] == "Data-Driven"
    assert state.onboarding_profile.ttfc_target_days == 2
    assert state.onboarding_profile.ttfp_target_days == 8
    assert "brutal_truth" in result
    
    print(f"  Strategy: {result['strategy']}")
    print(f"  Maturity: {result['maturity_level']}")
    print(f"  TTFC Target: {state.onboarding_profile.ttfc_target_days} days (automated)")
    print(f"  TTFP Target: {state.onboarding_profile.ttfp_target_days} days")
    print(f"  Brutal Truth: Present")
    print("  PASSED")

if __name__ == "__main__":
    test_startup_lean_onboarding()
    test_agile_structured_onboarding()
    test_enterprise_no_platform_onboarding()
    test_data_driven_platform_onboarding()

    print("\nALL ONBOARDING TESTS PASSED")
