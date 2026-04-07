# 🏛️ AI Architect Agent — Enterprise Operations Manual

**AI Architect** is a state-of-the-art deterministic decision engine designed for high-stakes enterprise architecture and regulatory compliance. It transforms raw project parameters into consultant-grade architectural dossiers, ensuring 100% professional alignment with European regulations (MiCA, PSD2, GDPR, DORA) and SRE best practices.

---

## 🎯 Project Vision
Unlike traditional chatbots, the AI Architect uses a **6-Layer Deterministic Pipeline** to guarantee consistency, auditability, and technical depth. It operates as a "Hybrid Engine" that orchestrates specialized intelligence plugins to solve complex trade-offs in distributed systems.

---

## 🏗️ System Architecture (The Hybrid Engine)

The system follows a strict hierarchical orchestration model:

### 1. The 6-Layer Request Lifecycle
1.  **Layer 0: Intake & Validation**: Sanitizes raw input and ensures data integrity.
2.  **Layer 1: Normalization**: Projects the project context into a standardized domain ontology.
3.  **Layer 2: Core Pattern Engine (Hybrid)**: 
    -   **Plugin Registry**: Auto-discovers and runs specialized intelligence plugins.
    -   **Legacy Core**: Reconciles results with established deterministic patterns.
4.  **Layer 3: Calculation Engine**: Performs financial modeling (LTV, CAC, NRR) and resource pricing.
5.  **Layer 4: Visual Engine**: Generates high-resolution architectural diagrams and clusters.
6.  **Layer 5: Validation & QCE**: Runs the **Qualitative Compliance Engine** to verify the integrity of the proposed solution.
7.  **Layer 6: Narrative Engine**: Forges the final institutional dossier (HTML/PDF).

### 2. The Orchestrator (`PipelineOrchestrator`)
The Orchestrator manages the transition from legacy deterministic code to the modern **Pillar Plugin** architecture. It ensures that plugins run first, injecting their "Intelligence Results" into the state before the legacy layers execute.

---

## 🔌 Plugin Development Manual

The system is extensible via the `orchestrator/plugins` directory.

### How to extend the AI Architect:
1.  **Define the Decision Tree**: Create a `knowledge/decision_tree.json` defining the nodes (questions), options, and leaves (strategies).
2.  **Implement the Plugin Logic**: Create a class inheriting from `BaseDecisionTreePlugin`.
3.  **Map Logic to Questions**: Implement `build_question_map` to link real-time metrics to decision tree nodes using Python lambdas.

```python
# Example routing logic in a plugin
def build_question_map(self, metrics, state):
    return {
        "root": lambda m: "high_load" if m.get("large_scale") else "standard",
        "sampling_check": lambda m: "yes" if m.get("latency_critical") else "no"
    }
```

---

## ⚖️ Regulatory & Compliance Manual

The AI Architect integrates deep domain knowledge for the primary European regulatory pillars:

### 🛡️ PSD2 & SCA (Payment Services)
-   **Deterministic Check**: Automatic identification of Payment/Fintech entities.
    -   **SCA Mandatory Baseline**: Forces Secure Customer Authentication requirements.
    -   **TRA Exemption Logic**: Implements RTS (Regulatory Technical Standards) thresholds for transaction risk analysis (exemptions for low-value/low-fraud transactions).

### 💎 MiCA & CNMV (Digital Assets)
-   **CASP Alignment**: Full decision tree for Crypto-Asset Service Providers.
    -   **Custody Segregation**: Enforces hot/cold wallet separation logic.
    -   **Whitepaper Validation**: Ensures compliance with MiCA disclosure requirements.

### 🔐 GDPR & Transparency
-   **Privacy by Design**: Mandatory DPIA (Data Protection Impact Assessment) triggering.
    -   **Crypto-Shredding Engine**: Recommends key-based deletion for forgotten users.
    -   **Cross-Border Assessment**: Identifies TIA (Transfer Impact Assessment) needs for US/Third-country transfers.

---

## 🛠️ Architectural Pillars Reference

### 🌋 SRE & Stability
-   **Chaos Engineering**: Auto-injects resilience testing strategies based on availability targets (99.9% vs 99.99%).
-   **SLO/SLA Modeling**: Hard-coded constraints for error budgets and MTTR.

### 🏎️ Performance Engineering
-   **Distributed Tracing**: Tail-based vs Head-based sampling logic based on transactional throughput.
-   **Load Testing**: Strictly differentiates between Soak Testing (Longevity) for Microservices and k6 CI/CD for standard SaaS.
-   **DB Optimization**: Transaction/Lock review vs Composite Indexing recommendations.

---

## 📊 Governance: QCE & Audit Trails

### Qualitative Compliance Engine (QCE)
The QCE evaluates the "Technical Debt vs Regulatory Risk" ratio. It produces:
-   **Institutional Integrity Seal**: A cryptographic-ready verification score.
-   **Evidence Vault**: A digital record of why each decision was made, linked to specific regulatory pillars (e.g., `AML_LEY_10_2010`).

---

## 🚀 Operations & Testing

### Installation
```bash
cd orchestrator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running the Suite (144+ Tests)
The system is protected by a massive verification suite ensuring zero regressions in architectural logic.
```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## 📝 License
Proprietary Enterprise Software. All rights reserved. 2026.
