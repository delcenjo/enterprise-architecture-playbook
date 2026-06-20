import json
import os
import logging
import hashlib
from typing import Dict, Any, List
from global_state import GlobalState

logger = logging.getLogger("Layer5_AuditEngine")
logging.basicConfig(level=logging.INFO)

class ValidationLayer:
    def __init__(self, state: GlobalState):
        self.state = state
        self.assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
        self.rules_path = os.path.join(self.assets_dir, "audit_rules.json")

    def run_layer_5(self):
        """
        Layer 5: Technical Audit & Risk Engine.
        Scores threats as Probability * Impact * Exposure, models resource bottlenecks,
        and produces a compliance grade.
        """
        logger.info("Starting Layer 5: Expert Technical Audit...")
        
        with open(self.rules_path, 'r') as f:
            rules = json.load(f)

        expert_audit = []
        global_risk_scores = []
        
        threats = rules.get("threat_profiles_2026", {})
        
        for key, threat in threats.items():
            prob = threat['probability'] # 0-5
            impact = threat['impact']     # 0-5
            exposure = 1.0
            driver = threat['resource_driver']
            
            if driver == "compute":
                vcpu = self.state.costs.get("raw_requirements", {}).get("compute", {}).get("vcpu", 0)
                if vcpu > 50: exposure += 0.5
            elif driver == "storage":
                vol = self.state.data_profile.volume_gb
                if vol > 1000: exposure += 0.4
            elif driver == "egress":
                egress = self.state.costs.get("raw_requirements", {}).get("networking", {}).get("egress_gb", 0)
                if egress > 500000: exposure += 0.6
            
            base_score = prob * impact * exposure
            mitigated_score = base_score * (1 - threat['mitigation_reduction'])
            
            expert_audit.append({
                "id": key,
                "name": threat['name'],
                "probability": prob,
                "impact": impact,
                "exposure": round(exposure, 2),
                "raw_score": round(base_score, 1),
                "mitigated_score": round(mitigated_score, 1),
                "coordinates": {"x": prob, "y": impact},
                "mitigation": rules['mitigations'].get(key, "Apply Well-Architected standard controls"),
                "critical_resource": driver.upper()
            })
            global_risk_scores.append(mitigated_score)

        vcpu_req = self.state.costs.get("raw_requirements", {}).get("compute", {}).get("vcpu", 0)
        if vcpu_req > 32:
            expert_audit.append({
                "id": "cpu_spikes",
                "name": "Predictive CPU Outage Risk",
                "probability": 3,
                "impact": 4,
                "exposure": 1.2,
                "raw_score": 14.4,
                "mitigated_score": 7.2,
                "coordinates": {"x": 3, "y": 4},
                "mitigation": "Enable EKS Vertical Pod Autoscaler (VPA)",
                "critical_resource": "COMPUTE"
            })

        self.state.technical_audit = expert_audit
        self.state.risk_matrix = expert_audit  # backward compatibility

        from layers.visual_engine import VisualEngine
        VisualEngine(self.state)._generate_risk_heatmap()

        # Compliance score: 100 minus the ratio of total mitigated risk to theoretical maximum.
        total_risk = sum(global_risk_scores)
        max_theoretical = len(threats) * 25
        self.state.compliance_score = max(0, 100 - (total_risk / max_theoretical * 100))
        
        self._freeze_with_integrity()

        logger.info(f"Layer 5 Expert Audit Complete. Resilience Index: {self.state.compliance_score:.1f}%")
        return f"Expert Audit complete. Sealed with Integrity Seal."

    def _freeze_with_integrity(self):
        self.state.freeze()
        state_data = self.state.model_dump_json().encode()
        state_hash = hashlib.sha256(state_data).hexdigest()
        self.state.costs["state_integrity_seal"] = state_hash
        logger.info(f"Integrity Seal Generated: {state_hash[:16]}...")

if __name__ == "__main__":
    from input_layer import PipelineManager
    from core_engine import CoreEngine
    from calculation_engine import CalculationEngine
    
    manager = PipelineManager()
    manager.run_layer_0_and_1({
        "business_type": "SaaS B2B",
        "expected_users_year1": 15000,
        "growth_rate": 0.5,
        "region": "US",
        "compliance_required": ["GDPR"],
        "availability_target": "99.99%",
        "data_sensitivity": "high"
    })
    CoreEngine(manager.state).run_layer_2()
    CalculationEngine(manager.state).run_layer_3()
    
    validator = ValidationLayer(manager.state)
    print(validator.run_layer_5())
    print(json.dumps(manager.state.risk_matrix, indent=2))
