# Changelog

All notable changes are documented here, following
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-22

### Added
- React + Vite + TypeScript frontend for entering a project and viewing results.
- Report builder: PDF / Excel / HTML output from the pipeline result.
- README with architecture, setup and usage.
- 37 test suites covering the decision engines.

## [0.8.0] - 2026-02-19

### Added
- Decision modules for finance (supply-chain security, LTV dynamics, unit economics),
  product (RICE prioritisation, OKR / DORA metrics, trade-off analysis),
  organisation (team topologies, platform engineering, cultural fit, seniority),
  engineering practices (tech debt, code review, scalability, fitness functions),
  performance (load testing, profiling, DB and frontend optimisation),
  SRE / observability (SLOs, distributed tracing, chaos engineering),
  and deployment / infrastructure (blue-green and canary, GitOps, IaC).
- Developer onboarding knowledge base.

## [0.5.0] - 2026-02-06

### Added
- Architecture-patterns knowledge base (ontology, decision trees, trade-off matrices).
- Regulatory knowledge base: GDPR, DORA, PSD2/SCA, AML/KYC, MiCA.
- Base operational ontology and decision framework.

## [0.3.0] - 2026-02-01

### Added
- 6-layer deterministic pipeline (intake → core → calculation → visuals → validation → narrative).
- Orchestrator with FastAPI and Pydantic state management.
- LLM reasoning with multi-provider support (Claude, GPT, Gemini) and a deterministic fallback.
- Simulation and workflow engines.

## [0.1.0] - 2026-01-17

### Added
- AWS pricing query API (FastAPI + PostgreSQL).
- AWS price ingestor with validation and normalisation.
- Database schema for pricing data.
- Docker Compose setup.

[1.0.0]: https://github.com/delcenjo/enterprise-architecture-playbook/compare/v0.8.0...v1.0.0
[0.8.0]: https://github.com/delcenjo/enterprise-architecture-playbook/compare/v0.5.0...v0.8.0
[0.5.0]: https://github.com/delcenjo/enterprise-architecture-playbook/compare/v0.3.0...v0.5.0
[0.3.0]: https://github.com/delcenjo/enterprise-architecture-playbook/compare/v0.1.0...v0.3.0
[0.1.0]: https://github.com/delcenjo/enterprise-architecture-playbook/releases/tag/v0.1.0
