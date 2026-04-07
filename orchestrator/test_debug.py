import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
from global_state import GlobalState, TrafficProfile
from layers.core_engine import CoreEngine

state = GlobalState()
engine = CoreEngine(state)
state.raw_input = {
    "business_type": "FINTECH_PAYMENTS",
    "remote_onboarding_enabled": True,
    "aml_geography_risk": 4, # High
    "aml_activity_risk": 4,  # High
    "aml_product_risk": 4,   # High
    "pii_operations_needed": True
}
# We don't call run_layer_2, we just run the metrics and traversal manually
adapted = engine._build_from_profile(engine._identify_profile())
metrics = engine._calculate_runtime_metrics(adapted, engine._identify_profile())
print("is_aml", metrics.get("is_aml_scope"))
print("req_kyc", metrics.get("requires_kyc_biometrics"))
print("req_mon", metrics.get("requires_aml_monitoring"))

import json
with open(engine.tree_path) as f: tree = json.load(f)

for p in ["aml_scope_check"]:
    curr = p
    while curr in tree['nodes']:
        print(f"visiting {curr}")
        node = tree['nodes'][curr]
        answer = "no"
        if curr == "aml_scope_check": answer = "yes" if metrics.get("is_aml_scope") else "no"
        elif curr == "kyc_method_evaluation": answer = "yes" if metrics.get("requires_kyc_biometrics") else "no"
        elif curr == "aml_monitoring_check": answer = "yes" if metrics.get("requires_aml_monitoring") else "no"
        print(f"answer for {curr}: {answer}")
        next_step = node['options'][answer]
        print(f"next step: {next_step}")
        if next_step in tree['leaves']:
            print(f"found leaf: {next_step}")
            break
        curr = next_step
