# Phase 10 — Frontend AI Governance Command Center

## Summary

Phase 10 adds a full visual command center for the Family Dollar AI Governance & Agentic Workflow Platform.

The previous frontend focused primarily on intake. This phase turns the frontend into a comprehensive demo surface for the full platform.

## What the Command Center Shows

- Platform status
- Completed phase map
- Governance risk-tier dashboard
- Retail system contracts
- Inventory system contract viewer
- Inventory replenishment agent runner
- Human approval workflow
- Policy gate tester
- Observability and cost dashboard
- Cost guardrail tester
- SOP/runbook/support handoff readiness
- Interview question prompts

## Backend Integration

The frontend calls the FastAPI backend at:

```text
http://localhost:8000

The following backend capabilities are surfaced visually:

/health
/v1/risk/tiers
/v1/governance/dashboard
/v1/retail/systems
/v1/retail/contracts/inventory
/v1/agents/inventory-replenishment/run
/v1/agents/inventory-replenishment/approval
/v1/policies/gates
/v1/policies/action-gate
/v1/observability/dashboard
/v1/observability/cost-guardrail
Demo Value

This phase makes the platform fully visual for interview demonstration. Instead of relying only on FastAPI Swagger docs and curl commands, the user can show a single command center that explains governance, architecture, agent workflows, controls, observability, and support handoff.

Local Run

Frontend dev mode:

cd frontend/intake-portal
npm run dev

Open:

http://localhost:5173

Docker Compose mode:

docker compose up

Open:

http://localhost:8080

Backend API docs:

http://localhost:8000/docs
Governance Principle

The command center visually reinforces the core platform rule:

AI may recommend, summarize, and draft. AI may not autonomously mutate retail systems, access payment data, bypass human approval, or bypass change control.
---
---
---
# Fix Backend Environment

Run this from Terminal 1:

```bash
cd ~/family-dollar-ai-governance-platform-lab/backend/governance-api

echo "=== current directory ==="
pwd

echo "=== existing files ==="
ls -la

echo "=== check dependency files ==="
find . -maxdepth 2 -type f \( -name "requirements.txt" -o -name "pyproject.toml" -o -name "poetry.lock" -o -name "Pipfile" \) -print
Then create the missing backend virtual environment:

bash
cd ~/family-dollar-ai-governance-platform-lab/backend/governance-api

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
Now install dependencies. Use this first:

bash
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
elif [ -f pyproject.toml ]; then
  pip install -e .
else
  pip install fastapi "uvicorn[standard]" pydantic python-dotenv
fi
Verify FastAPI is available:

bash
python - <<'PY'
import fastapi
import uvicorn

print("fastapi OK:", fastapi.__version__)
print("uvicorn OK")
PY
Start backend again:

bash
cd ~/family-dollar-ai-governance-platform-lab/backend/governance-api
source .venv/bin/activate

uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
Test From Another Terminal
bash
curl http://localhost:8001/health
Expected:

json
{"status":"ok","service":"family-dollar-ai-governance-api","phase":"2"}
Update Your Runbook Correction
Replace this backend block:

bash
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
with this safer version:

bash
cd ~/family-dollar-ai-governance-platform-lab/backend/governance-api

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install --upgrade pip

if [ -f requirements.txt ]; then
  pip install -r requirements.txt
elif [ -f pyproject.toml ]; then
  pip install -e .
else
  pip install fastapi "uvicorn[standard]" pydantic python-dotenv
fi

uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
Important Rule
One important rule going forward: for this project, always activate the backend venv from:

text
~/family-dollar-ai-governance-platform-lab/backend/governance-api/.venv
