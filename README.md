# Enterprise Architecture Playbook

![CI](https://github.com/delcenjo/enterprise-architecture-playbook/actions/workflows/ci.yml/badge.svg)

A deterministic decision-support engine for cloud architecture and regulatory
compliance. Given a project's parameters (scale, domain, constraints), it runs a
multi-layer pipeline that recommends architecture patterns, checks compliance
requirements, estimates cost, and produces a structured report.

Large language models are used **only** to turn the deterministic results into a
written narrative — the decisions themselves are rule-based and reproducible.

> Personal project built to practise domain-driven / hexagonal design, a plugin
> architecture and multi-service orchestration with Docker.

## Components

| Service | Stack | Responsibility |
| ------- | ----- | -------------- |
| `api` | FastAPI + PostgreSQL | Query normalised AWS pricing / instance data |
| `ingestor` | Python + boto3 | Fetch, validate and normalise AWS price data into the database |
| `intelligence` | FastAPI + litellm | LLM-assisted reasoning (Claude / GPT / Gemini) with caching and a mock fallback |
| `orchestrator` | FastAPI (hexagonal) | Core decision pipeline and plugins |
| `output_generator` | Python | Build HTML / PDF / Excel reports and IaC / ADR templates |
| `frontend` | React + TypeScript + Vite | Dashboard to enter a project and view the result |

## The decision pipeline

The orchestrator processes a request in ordered layers:

0. **Intake & validation** — sanitise and validate the input.
1. **Normalisation** — map the input to a common domain model.
2. **Core engine** — run decision-tree plugins (compliance, SRE, performance,
   organisation, finance) and reconcile them with deterministic rules.
3. **Calculation** — financial modelling (TCO, LTV/CAC, unit economics).
4. **Visuals** — generate diagrams and charts.
5. **Validation** — a qualitative compliance check over the proposed solution.
6. **Narrative** — render the final report (LLM if an API key is set, otherwise a
   deterministic template).

Plugins follow a ports-and-adapters layout, so new decision domains can be added
without touching the core.

## Tech stack

Python, FastAPI, PostgreSQL, litellm, React + TypeScript + Vite, Docker Compose.

## Running locally

```bash
docker compose up        # services + PostgreSQL
```

Or per service:

```bash
cd orchestrator && pip install -r requirements.txt && uvicorn main:app --port 8003
cd api          && pip install -r requirements.txt && uvicorn price_query_api:app --port 8000
cd frontend     && npm install && npm run dev
```

The LLM narrative is optional: set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` to
enable it; without a key the engine falls back to a deterministic template.

## Tests

```bash
cd orchestrator && python -m unittest discover -s tests -p "test_*.py"
```

37 suites cover the decision engines: compliance (GDPR, PSD2/SCA, AML, MiCA),
SRE and observability, performance, organisation and financial modelling.

## Repository layout

```
api/              pricing query service
ingestor/         AWS price ETL
intelligence/     LLM reasoning service
orchestrator/     core decision pipeline (domain / application / adapters)
output_generator/ report and template builder
frontend/         React dashboard
```
