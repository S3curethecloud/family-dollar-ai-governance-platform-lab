# 5-Minute Interview Demo Script

## Opening — 30 seconds

"I built this Family Dollar AI Governance & Agentic Workflow Platform to demonstrate how I would operate as an AI Solutions Architect and Governance Lead. The platform covers the lifecycle from intake to risk-tiering, architecture review, retail system integration, agentic workflow execution, policy gates, observability, cost controls, deployment readiness, and IT support handoff."

## Step 1 — Governance Intake Portal

"First, I created the intake portal because enterprise AI governance should start before a model is built. The portal captures business unit, use case, retail system touched, data sensitivity, customer/payment data exposure, autonomy level, dependencies, release window, and expected business value."

Key message:

"Intake gives the governance forum and architecture team enough context to prioritize safely."

## Step 2 — Risk-Tiering Engine

"Next, I added a backend governance API. It evaluates requests using transparent rules and returns risk tier, risk score, required reviews, blocked reasons, owner team, and recommended next step."

Key message:

"The decision is explainable. It does not replace governance review, but it accelerates consistent triage."

## Step 3 — Retail System APIs and Contracts

"I then modeled Family Dollar's retail IT estate with APIs and data contracts for POS, inventory, ERP, CRM, supply chain, and identity."

Key message:

"AI does not get direct system access. It integrates through governed APIs with owner teams, auth requirements, logging, allowed operations, forbidden operations, and risk classifications."

## Step 4 — Inventory Replenishment Agent

"The first agentic workflow is an Inventory Replenishment Assistant. It reads low-stock inventory, checks POS demand signals, checks supply-chain constraints, generates reorder recommendations, and logs each step."

Key message:

"The agent can recommend, but it cannot create purchase orders, mutate inventory, or execute supplier actions."

## Step 5 — Policy Gates

"I added policy gates for prompt approval, deployment readiness, retail action safety, environment promotion, and human approval."

Key message:

"Governance is enforceable, not just documentation. Autonomous retail-system execution is denied by policy."

## Step 6 — Observability and Cost Controls

"The observability layer tracks traces, tool calls, latency, token estimates, cost estimates, guardrail status, and approval state."

Key message:

"This is how I would optimize agentic workflows at scale and minimize compute waste."

## Step 7 — Deployment and Handoff

"Finally, I containerized the backend and frontend, added Docker Compose, CI, and Terraform scaffolding for GCP Cloud Run. I also added SOPs, runbooks, rollback, incident escalation, prompt/model versioning, and support handoff."

Key message:

"This shows the full lifecycle: build, govern, deploy, operate, and transition to IT support."

## Close

"This platform demonstrates the way I would lead AI delivery at Family Dollar: build hands-on, integrate with existing systems, govern risk, enforce controls, measure operations, and hand off responsibly."
