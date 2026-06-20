# Contributing

Contributions are welcome. Please open a pull request from a feature branch.

## Setup

To run the core decision engine:

```bash
cd orchestrator
pip install -r requirements.txt
```

The full stack (services + PostgreSQL) runs with Docker:

```bash
docker compose up
```

## Tests

```bash
cd orchestrator
python -m unittest discover -s tests -p "test_*.py"
```

## Workflow

- Branch from `main` and keep each pull request focused on a single change.
- Add or update tests for any behaviour you change.
- Make sure the test suite passes before opening the pull request.

## Style

- Follow the existing domain-driven / hexagonal layout.
- Keep comments meaningful and concise.
