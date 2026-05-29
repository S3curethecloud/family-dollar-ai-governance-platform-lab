# Interview Study Guide

## Role target

**AI Solutions Architect and Governance Lead**

This guide turns the platform build into interview preparation. Each section includes likely questions and strong answer themes.

## Your core positioning

Use this positioning repeatedly:

> I operate as a hands-on AI architect who can translate business requirements into working AI applications, define integration patterns across enterprise systems, and run the governance process that keeps delivery fast, secure, and operationally supportable.

## Platform elevator pitch

> I built a retail AI governance and agentic workflow platform that simulates how a company like Family Dollar could intake AI requests, risk-tier them, map dependencies across POS, inventory, CRM, ERP, and supply-chain systems, recommend GCP-style architecture patterns, run approval-gated agent workflows, track model and prompt versions, capture trace and cost telemetry, and transition solutions to IT support through SOPs and runbooks.

## Section 1 — Business requirements to AI solution architecture

### Likely questions

- Walk me through how you would take a business AI request from idea to implementation.
- How do you translate vague business requirements into a target AI solution?
- How do you decide whether a use case needs RAG, an agent, a workflow, or a traditional application?
- How do you deliver fast without skipping architecture discipline?

### Answer themes

- Start with business outcome, operational context, and measurable success criteria.
- Identify data sources, system owners, user roles, risk, dependencies, and integration pattern.
- Prototype the riskiest assumption first.
- Use an iterative path: intake, triage, architecture, prototype, evaluation, release readiness, handoff.
- Avoid overengineering early; choose Cloud Run-style delivery for fast iteration unless complexity requires GKE.

### Strong answer phrase

> I start by turning the request into a delivery contract: business outcome, impacted systems, data sensitivity, user workflow, model pattern, risk tier, integration dependencies, release window, and operating model.

## Section 2 — Google Cloud Platform architecture

### Likely questions

- How would you build AI applications on GCP?
- When would you choose Cloud Run versus GKE?
- How would you use Vertex AI or Gemini in this architecture?
- How would you handle secrets, IAM, and environment promotion?

### Answer themes

- Cloud Run for fast, containerized APIs and workflow services.
- Vertex AI/Gemini for model access and managed AI capabilities.
- Cloud SQL or Firestore for operational state.
- BigQuery for governance analytics and cost/risk reporting.
- Secret Manager for credentials.
- Cloud Logging and Monitoring for observability.
- Terraform and CI/CD for repeatable deployment.
- GKE only when advanced orchestration, isolation, service mesh, or platform standards require it.

### Strong answer phrase

> For the first production-shaped release, I would favor Cloud Run because it gives speed, lower operational burden, autoscaling, and strong integration with IAM, logging, and CI/CD. I would move to GKE only when platform requirements justify that complexity.

## Section 3 — Retail system integration

### Likely questions

- How would AI integrate with POS, ERP, CRM, inventory, and supply-chain systems?
- What would you require before connecting an AI workflow to a retail system?
- How do you avoid AI becoming a shadow system of record?
- What belongs in a data contract?

### Answer themes

- Use approved APIs, not uncontrolled direct database access.
- Define owner, SLA, auth model, data classification, logging, allowed operations, forbidden operations, and rollback notes.
- Treat AI as recommendation/orchestration, not the source of truth.
- Start read-only; move to approval-gated writes only after controls are proven.

### Strong answer phrase

> My first rule is that retail systems remain systems of record. AI can summarize and recommend, but any operational write must go through an approved API, a system owner, policy checks, audit, and rollback planning.

## Section 4 — AI governance intake and forum leadership

### Likely questions

- How would you run an AI governance forum?
- How would you triage and prioritize AI requests?
- How do you balance innovation and risk control?
- What metrics would you show leadership?

### Answer themes

- Intake should capture value, risk, criticality, data sensitivity, systems touched, autonomy, human oversight, dependencies, and release window.
- Governance should route and accelerate, not just block.
- Use risk tiers to determine review depth.
- Dashboard should show open requests, approved/rejected items, high-risk requests, blocked dependencies, release windows, cost trend, risk trend, and post-implementation reviews.

### Strong answer phrase

> I would run governance as a portfolio operating model: every request has value, risk, dependencies, release status, owner, and next decision visible in one place.

## Section 5 — Risk tiering

### Likely questions

- How would you classify AI use cases into risk tiers?
- What makes an AI request high risk?
- How would you handle PII or payment data?
- What use cases require executive review?

### Answer themes

- Tier 1: low-risk internal productivity.
- Tier 2: moderate internal operational use.
- Tier 3: customer impact, operational dependency, sensitive data, or approval-gated execution.
- Tier 4: payment data, high autonomy, employment impact, material financial/customer risk.
- More risk means more evidence, approvers, testing, rollback, and monitoring.

### Strong answer phrase

> I tier by data sensitivity, customer impact, operational criticality, autonomy, integration complexity, and reversibility.

## Section 6 — Agentic workflow safety

### Likely questions

- How would you design an agentic workflow safely?
- How do you prevent unauthorized autonomous action?
- What state should you track in agent workflows?
- How do you control tool use?

### Answer themes

- Keep system prompts separate from policy enforcement.
- Use tool allowlists and explicit action boundaries.
- Track session, workflow, agent, tool call, prompt version, model version, cost, latency, approval state, and policy decision.
- Require human or policy approval before operational execution.
- Fail closed if policy/approval state is missing.

### Strong answer phrase

> I do not rely on prompt instructions as the control plane. The control plane is policy, identity, approval state, API permissions, and audit logging.

## Section 7 — State, tracing, and cost control

### Likely questions

- How do you optimize state management across agentic workflows?
- How do you minimize compute waste?
- What telemetry would you capture?
- How would you debug a bad AI recommendation?

### Answer themes

- Persist workflow state and tool-call state separately.
- Limit tool loops and retries.
- Track token estimates, cost estimates, latency, failure rate, and model choice.
- Use prompt/model versions to reproduce behavior.
- Use trace IDs to connect intake, workflow, API calls, approval, and output.

### Strong answer phrase

> I want every recommendation to be reproducible: which request, which data, which prompt, which model, which tools, which policy decision, which approver, and what cost.

## Section 8 — Prompt/model versioning and change control

### Likely questions

- How would you govern prompt changes?
- Are prompts code or configuration?
- How do you promote model changes across environments?
- How would you roll back a bad prompt?

### Answer themes

- Prompts are versioned release artifacts when they affect production behavior.
- Track owner, version, evaluation result, approval status, release date, rollback version, and limitations.
- Promote through dev/test/prod with approval gates.
- Roll back prompt/model versions independently where possible.

### Strong answer phrase

> If a prompt changes production behavior, I treat it like a governed artifact with versioning, evaluation, approval, deployment, and rollback.

## Section 9 — IT support handoff and operations

### Likely questions

- How do you transition support to IT?
- What should be in the runbook?
- How do you remain accountable after handoff?
- What dashboards and alerts are needed?

### Answer themes

- Handoff requires named owners, runbook, SOP, dashboards, alerts, known issues, rollback process, escalation path, and support training.
- The architect remains escalation owner for design-level issues.
- Post-implementation review captures business outcome and operational lessons.

### Strong answer phrase

> I consider delivery incomplete until support can detect, triage, escalate, and roll back the solution without needing the builder for routine operations.

## Section 10 — Questions to ask Family Dollar

Ask thoughtful questions that show architecture and governance maturity:

1. What GCP services are already approved for AI workloads?
2. Is Vertex AI/Gemini already part of the enterprise AI platform strategy?
3. What systems are highest priority for AI integration: POS, inventory, supply chain, CRM, ERP, store operations, or IT support?
4. Does the organization already have AI risk tiers, or would this role define them?
5. What is the current intake process for AI requests?
6. Who sits in the governance forum today?
7. How are prompt/model changes currently reviewed and promoted?
8. What are the biggest blockers to AI delivery: data access, platform readiness, security review, business clarity, or support handoff?
9. What does success look like in the first 90 days?
10. Which AI use case would you want this role to prototype first?

## 30-second closing pitch

> My value is that I can operate across the whole lifecycle. I can sit with the business to clarify the use case, define the GCP architecture, build the prototype, create the integration contracts, establish the governance path, instrument the workflow, control cost and risk, and then hand it over to IT with runbooks and dashboards. That is exactly why I built this lab: to show the full operating model, not just a chatbot demo.
