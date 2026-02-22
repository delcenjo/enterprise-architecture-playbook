# 🏛️ AI Architect — Enterprise Decision Engine

**Sistema de IA determinístico** que genera diagnósticos de arquitectura de software de nivel consultoría ($100k+), combinando motores de cálculo financiero, compliance regulatorio (GDPR, DORA, PSD2, AML), y 35+ pilares de ingeniería avanzada.

> **No es un chatbot.** Es un motor de decisión estructurado que produce dossiers técnicos con la profundidad de un CTO senior.

---

## 📐 Arquitectura del Sistema

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────┐
│   Frontend   │────▶│   Orchestrator   │────▶│  Intelligence │
│  React/Vite  │     │  FastAPI (8003)   │     │  LLM Engine   │
└─────────────┘     └──────────────────┘     └──────────────┘
                           │                        │
                    ┌──────┴──────┐          ┌──────┴──────┐
                    │  Knowledge  │          │   Output    │
                    │  Base (JSON)│          │  Generator  │
                    └─────────────┘          └─────────────┘
                                                    │
                                             ┌──────┴──────┐
                                             │   Pricing   │
                                             │  API + DB   │
                                             └─────────────┘
```

| Servicio | Puerto | Tecnología |
|---|---|---|
| **Frontend** | `8080` | React 19 + Vite + TypeScript + Tailwind CSS |
| **Orchestrator** | `8003` | FastAPI + Pydantic + 6-Layer Deterministic Pipeline |
| **Intelligence** | `8001` | LLM Engine (Claude/GPT/Gemini + Ollama fallback) |
| **Output Generator** | `8002` | PDF/Excel Builder |
| **Pricing API** | `8000` | FastAPI + PostgreSQL |
| **Database** | `5433` | PostgreSQL 15 |

---

## 🚀 Instalación y Puesta en Marcha

### Prerrequisitos

- [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/install/)
- [Node.js 18+](https://nodejs.org/) (solo para desarrollo frontend local)
- [Python 3.11+](https://www.python.org/) (solo para desarrollo backend local)
- Acceso a al menos una API de LLM (Anthropic, OpenAI, o Google Gemini)

### Opción 1: Docker Compose (Recomendado — Producción)

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/proyecto_ia.git
cd proyecto_ia

# 2. Configurar variables de entorno
cp orchestrator/.env.example orchestrator/.env
# Editar orchestrator/.env con tus API keys reales

# 3. Levantar todos los servicios
docker-compose up --build -d

# 4. Verificar que todos los contenedores están corriendo
docker-compose ps
```

Acceder a:
- **Frontend**: [http://localhost:8080](http://localhost:8080)
- **API del Orchestrator**: [http://localhost:8003/docs](http://localhost:8003/docs)

### Opción 2: Desarrollo Local (Sin Docker)

#### Backend (Orchestrator)

```bash
# 1. Crear y activar virtual environment
cd orchestrator
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
# venv\Scripts\activate    # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar entorno
cp .env.example .env
# Editar .env con tus API keys

# 4. Lanzar el servidor
uvicorn main:app --host 0.0.0.0 --port 8003 --reload
```

#### Frontend

```bash
# 1. Instalar dependencias
cd frontend
npm install

# 2. Lanzar en modo desarrollo
npm run dev
```

El frontend estará disponible en [http://localhost:5173](http://localhost:5173).

#### Base de datos (PostgreSQL)

```bash
# Opción rápida con Docker solo para la BD
docker run -d \
  --name pricing_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=pricing \
  -p 5433:5432 \
  -v $(pwd)/init.sql:/docker-entrypoint-initdb.d/init.sql \
  postgres:15
```

---

## 📊 Pilares del Motor de Decisión (35+)

El sistema integra más de 35 dimensiones de análisis en su pipeline determinístico:

| Categoría | Pilares |
|---|---|
| **Arquitectura** | Patterns, CQRS, Sharding, Multi-Region, Service Mesh |
| **Compliance** | GDPR, DORA, PSD2/SCA, AML/KYC, CNMV/MiCA, BdE 4/2017 |
| **Operaciones** | Observability, SRE/SLOs, Tracing, Chaos Engineering |
| **Deployment** | Blue-Green, Canary, Feature Flags, GitOps, IaC |
| **Seguridad** | Supply Chain (SBOM/SLSA), DPIA, Cross-Border Transfers |
| **Performance** | Load Testing, Profiling, DB Optimization, Frontend Vitals |
| **Ingeniería** | Tech Debt, Code Review, Fitness Functions, Scalability |
| **Producto** | TPM/RICE, OKRs/DORA, Trade-off Analysis |
| **Organización** | Platform Engineering, Team Topologies, Senior Evaluation, Cultural Fit, **Developer Onboarding** |

---

## 🗂 Estructura del Proyecto

```
proyecto_ia/
├── frontend/              # React + Vite + TypeScript + Tailwind
│   ├── src/App.tsx        # 7-Block Enterprise Decision UI
│   └── package.json
├── orchestrator/          # Core Deterministic Engine
│   ├── main.py            # FastAPI + Pydantic schemas
│   ├── global_state.py    # State management models
│   ├── main_pipeline.py   # 6-layer pipeline runner
│   ├── layers/            # Processing layers
│   │   ├── input_layer.py     # Layer 0-1: Validation + Normalization
│   │   ├── core_engine.py     # Layer 2: 31-pass Pattern Engine
│   │   ├── calculation_engine.py
│   │   ├── visual_engine.py
│   │   ├── validation_layer.py
│   │   └── narrative_engine.py
│   ├── knowledge/         # JSON Knowledge Bases
│   │   ├── patterns/      # Architecture decision trees
│   │   ├── regulatory/    # GDPR, DORA, PSD2, AML, CNMV
│   │   └── ops/           # 25+ operational pillars
│   ├── tests/             # Verification suites (35+ test files)
│   ├── requirements.txt
│   └── .env.example       # ⚠️ Copiar a .env con tus keys
├── intelligence/          # LLM Narrative Engine
├── api/                   # Cloud Pricing API
├── ingestor/              # AWS Price Data Ingestor
├── output_generator/      # PDF/Excel Dossier Builder
├── docker-compose.yml     # Full stack orchestration
├── init.sql               # PostgreSQL schema
└── .gitignore
```

---

## ⚙️ Variables de Entorno

Copiar `orchestrator/.env.example` → `orchestrator/.env` y configurar:

| Variable | Descripción | Ejemplo |
|---|---|---|
| `PREMIUM_LLM_PROVIDER` | LLM principal para narrativas | `claude`, `gemini`, `openai` |
| `ANTHROPIC_API_KEY` | API Key de Anthropic | `sk-ant-...` |
| `GEMINI_API_KEY` | API Key de Google | `AIza...` |
| `OPENAI_API_KEY` | API Key de OpenAI | `sk-...` |
| `USE_LOCAL_FALLBACK` | Usar Ollama si fallan las APIs | `true` / `false` |
| `LOCAL_OLLAMA_MODEL` | Modelo local de fallback | `qwen2.5:14b` |

---

## 🧪 Tests

```bash
# Ejecutar todos los tests del motor determinístico
cd orchestrator
source venv/bin/activate
python -m pytest tests/ -v

# O ejecutar un test individual
python tests/test_onboarding_engine.py
```

---

## 📝 Licencia

Proyecto privado. Todos los derechos reservados.
