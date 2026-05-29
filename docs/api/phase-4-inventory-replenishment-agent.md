# Phase 4 — Inventory Replenishment Assistant

## Summary

Phase 4 adds the first agentic workflow to the Family Dollar AI Governance & Agentic Workflow Platform.

The Inventory Replenishment Assistant reads governed retail APIs, analyzes low-stock inventory, checks demand and supply-chain signals, generates reorder recommendations, records trace events, estimates cost, and enforces human approval before any operational handoff.

## Why This Matters

The AI Solutions Architect and Governance Lead role requires building AI applications hands-on while also optimizing state management, tracing, cost controls, and governance across agentic workflows.

This phase demonstrates:

- Agent workflow orchestration
- Retail API integration
- State tracking
- Tool-call tracing
- Token and cost estimates
- Human approval gates
- Execution boundaries
- No autonomous retail-system mutation

## Agent Workflow

1. Inspect low-stock inventory.
2. Check POS demand signals using aggregated sales summary only.
3. Check supply-chain constraints.
4. Generate reorder recommendations.
5. Enforce approval gate.
6. Record approval or rejection decision.

## API Endpoints Added

| Method | Path | Purpose |
|---|---|---|
| POST | `/v1/agents/inventory-replenishment/run` | Run inventory replenishment agent |
| GET | `/v1/agents/inventory-replenishment/workflows/{workflow_id}` | Retrieve workflow state |
| POST | `/v1/agents/inventory-replenishment/approval` | Approve or reject workflow handoff |

## Governance Boundaries

- AI can recommend reorder actions.
- AI cannot place purchase orders.
- AI cannot mutate inventory records.
- AI cannot modify supplier records.
- AI cannot execute POS or ERP actions.
- Human approval is required before handoff.
- Even after approval, autonomous execution remains blocked in this demo.

## Demo Talk Track

"At this phase I added the first agentic workflow: an Inventory Replenishment Assistant. It reads controlled retail APIs, generates reorder recommendations, logs every workflow step, estimates tokens and cost, and enforces a human approval gate. The important design point is that the agent can recommend, but it cannot execute operational actions or mutate enterprise systems. That is the governance boundary I would apply before scaling agentic workflows in a real retail environment."

## Likely Interview Questions

1. How would you design an agentic workflow for inventory replenishment?
2. How do you track state across agent steps?
3. What should be logged for each tool call?
4. How would you estimate or control compute cost?
5. How do you prevent autonomous purchase orders?
6. How does this workflow use POS, inventory, and supply-chain data?
7. What happens after a human approves a recommendation?
8. How would you hand this workflow off to IT support?
9. How would you extend this into a real GCP deployment?
10. How would you monitor failures, latency, and business impact?
