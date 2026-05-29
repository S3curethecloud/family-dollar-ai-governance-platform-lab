# Demo Script

## Demo title

**Family Dollar — Retail AI Governance & Agentic Workflow Platform**

## Demo objective

Show that the platform can manage the full lifecycle of a retail AI use case: intake, risk tiering, dependency mapping, architecture recommendation, governance approval, agent workflow, traceability, cost controls, and IT handoff.

## Opening script

> This demo shows how I would approach the AI Solutions Architect and Governance Lead role. Instead of building only a chatbot, I built the control plane around enterprise AI delivery: intake, governance, risk tiering, retail integration contracts, agentic workflow safety, observability, cost control, rollback, and IT support handoff.

## Problem setup

> In a retail environment, AI opportunities arrive from many teams: store operations, inventory, supply chain, CRM, finance, customer support, and IT support. The challenge is not just building AI quickly. The challenge is building it safely, integrating it into existing systems, governing risk, and making it supportable after launch.

## Walkthrough part 1 — Intake

Say:

> The first surface is the governance intake portal. A business user submits the AI use case, affected systems, data sensitivity, business value, autonomy level, dependencies, and target release window.

Point out:

- Business unit.
- Use case description.
- Retail systems touched.
- Data sensitivity.
- Customer/payment data indicators.
- Operational impact.
- Expected business value.
- Autonomous action level.
- Human approval requirement.
- Dependencies and release window.

Leadership message:

> This gives the governance forum structured data instead of vague AI ideas in email threads.

## Walkthrough part 2 — Risk tiering

Say:

> Once submitted, the platform classifies the request into a risk tier. The risk model considers data sensitivity, customer impact, operational dependency, integration complexity, autonomy, and whether human approval is required.

Use this explanation:

- Tier 1: low-risk internal productivity.
- Tier 2: moderate internal operations.
- Tier 3: high-risk operational or customer-impacting use.
- Tier 4: restricted, executive/security/legal review.

Leadership message:

> Governance is not treated as a blocker. It is a routing mechanism that determines the right level of review.

## Walkthrough part 3 — Retail integration mapping

Say:

> The platform identifies impacted retail systems and the required integration pattern. For the inventory replenishment assistant, the first version uses read-only access to inventory, demand, and supply-chain signals. Execution is blocked until a human approval flow exists.

Point out:

- POS as demand signal source.
- Inventory as stock-level source.
- Supply chain as delay/source availability signal.
- ERP as future purchase-order integration.
- Identity as approval role source.

Leadership message:

> Retail systems remain systems of record. The AI layer recommends; it does not become the operational source of truth.

## Walkthrough part 4 — Agentic workflow

Say:

> The first agentic workflow is an Inventory Replenishment Assistant. It can inspect inventory, detect low stock, check demand indicators, assess supply-chain risk, and recommend a reorder. But it cannot execute the reorder without approval.

Point out required trace fields:

- session_id.
- workflow_id.
- agent_id.
- tool_call_id.
- prompt_version.
- model_version.
- token_estimate.
- cost_estimate.
- latency_ms.
- approval_status.
- rollback_status.

Leadership message:

> I do not rely on prompt instructions as the control plane. The actual controls are policy, identity, approval state, API permissions, and audit logs.

## Walkthrough part 5 — Governance dashboard

Say:

> The governance dashboard gives the forum a portfolio view: open requests, approved requests, rejected requests, high-risk items, blocked dependencies, release windows, cost trends, risk trends, and post-implementation review status.

Leadership message:

> This gives leadership a way to manage AI delivery as a portfolio instead of a collection of experiments.

## Walkthrough part 6 — Handoff and runbooks

Say:

> The final part is support readiness. A solution is not done when the model works. It is done when IT support has SOPs, runbooks, dashboards, alerts, rollback steps, known limitations, and escalation paths.

Point out:

- AI Intake SOP.
- Risk Tiering Runbook.
- Agent Deployment Runbook.
- Rollback Runbook.
- Incident Escalation Runbook.
- Prompt Versioning SOP.
- Model Promotion SOP.
- Support Handoff Checklist.

Leadership message:

> I remain the architectural escalation point after handoff, but routine support should be operationalized.

## Strong closing

> This demo is intentionally broader than a single AI app. It shows the operating model required to scale AI responsibly: intake, architecture, governance, engineering, tracing, cost control, policy, deployment, and support. That is the value I would bring to Family Dollar as an AI Solutions Architect and Governance Lead.

## Five-minute version

1. Open with the platform purpose.
2. Show intake fields.
3. Explain risk tiering.
4. Explain retail integration contracts.
5. Walk through the inventory replenishment agent.
6. Show why approval gates matter.
7. Close with support handoff and governance dashboard.

## Two-minute version

> I built this as a GCP-style retail AI governance platform. It starts with intake, classifies risk, maps retail system dependencies, recommends architecture patterns, and then runs an approval-gated agent workflow. The first workflow is inventory replenishment: it can analyze stock, demand, and supply-chain signals, but it cannot execute without human approval. Everything is traced: prompt version, model version, tool calls, latency, cost, approval state, and rollback state. The platform also includes the governance dashboard and support handoff model, because enterprise AI delivery requires more than model output; it requires operating discipline.

## Questions to invite

At the end, ask:

- “Would you like me to go deeper on the GCP deployment architecture?”
- “Would you like me to walk through the risk tiering logic?”
- “Would you like me to explain how I would transition this from prototype to IT support?”
