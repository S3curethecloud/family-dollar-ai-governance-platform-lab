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
