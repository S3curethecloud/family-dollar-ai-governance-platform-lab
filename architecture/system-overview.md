# System Overview

## Purpose

This platform is a governed AI application delivery control plane for a retail enterprise. It demonstrates how AI use cases can move from business intake through risk tiering, architecture review, approval, prototype, deployment, observability, support handoff, and post-implementation review.

The system is designed for an AI Solutions Architect and Governance Lead who must be both a hands-on builder and a governance owner.

## Primary users

| User | Responsibility |
|---|---|
| Business requester | Submit AI opportunities and business requirements |
| AI governance lead | Triage, risk-tier, prioritize, and route requests |
| Solution architect | Define target architecture, integrations, APIs, data contracts, and delivery path |
| Security team | Review data sensitivity, identity, policy, audit, and risk controls |
| Data team | Validate data availability, quality, lineage, and analytical dependencies |
| Platform team | Own cloud runtime, CI/CD, networking, environment promotion, and observability |
| Application owners | Own POS, inventory, CRM, ERP, supply-chain, and store operations systems |
| IT support | Operate approved solutions after structured handoff |

## Logical architecture

```text
+--------------------+
| Business Requester |
+---------+----------+
          |
          v
+-----------------------------+
| AI Governance Intake Portal |
+-------------+---------------+
              |
              v
+-----------------------------+        +--------------------------+
| Governance API              |------->| Risk Tiering Engine      |
| - intake submission         |        | - business impact score  |
| - request state             |        | - data risk score        |
| - approval routing          |        | - autonomy risk score    |
+-------------+---------------+        +------------+-------------+
              |                                     |
              v                                     v
+-----------------------------+        +--------------------------+
| Governance Forum Dashboard  |<-------| Policy Gate Service      |
| - portfolio view            |        | - approval checks        |
| - release windows           |        | - restricted actions     |
| - dependencies              |        | - promotion gates        |
| - post-implementation review|        +------------+-------------+
+-------------+---------------+                     |
              |                                     v
              |                       +--------------------------+
              |                       | Agent Workflow Runtime   |
              |                       | - state                  |
              |                       | - tool calls             |
              |                       | - prompt/model versions  |
              |                       | - approval state         |
              |                       +------------+-------------+
              |                                    |
              v                                    v
+-----------------------------+        +--------------------------+
| Architecture Recommendation |        | Mock Retail APIs         |
| - GCP pattern               |        | - POS                    |
| - integration dependencies  |        | - Inventory              |
| - environment strategy      |        | - ERP                    |
| - rollback pattern          |        | - CRM                    |
+-----------------------------+        | - Supply Chain           |
                                       | - Identity               |
                                       +------------+-------------+
                                                    |
                                                    v
                                       +--------------------------+
                                       | Observability + Audit    |
                                       | - traces                 |
                                       | - cost estimates         |
                                       | - latency                |
                                       | - approval decisions     |
                                       | - rollback state         |
                                       +--------------------------+
```

## Target GCP implementation model

| Capability | Initial demo implementation | GCP-style production mapping |
|---|---|---|
| Web application | Next.js intake portal | Cloud Run or Firebase Hosting |
| API backend | FastAPI service | Cloud Run or GKE |
| AI orchestration | Custom workflow engine or LangGraph-style state machine | Cloud Run services, Workflows, Pub/Sub |
| Model access | Gemini/Vertex abstraction | Vertex AI / Gemini API |
| Operational data | Local JSON/PostgreSQL-style schema | Cloud SQL or Firestore |
| Analytics | Governance dashboard events | BigQuery and Looker Studio |
| Search/RAG | Placeholder retrieval contract | Vertex AI Search or pgvector |
| Identity | Mock approver roles | IAM, Identity Platform, Workforce Identity Federation |
| Secrets | Environment variables in demo | Secret Manager |
| Observability | Structured trace events | Cloud Logging, Cloud Monitoring, OpenTelemetry |
| CI/CD | GitHub Actions | Cloud Build / Cloud Deploy option |
| Infrastructure | Terraform skeleton | Terraform for GCP projects, IAM, Cloud Run, Cloud SQL, logging sinks |

## Core domain objects

### AI intake request

Represents a submitted business use case.

Key fields:

- request_id.
- title.
- business_unit.
- use_case_description.
- retail_systems_touched.
- data_sensitivity.
- customer_data_involved.
- payment_data_involved.
- operational_impact.
- expected_business_value.
- model_type.
- autonomous_action_level.
- human_approval_required.
- dependencies.
- target_release_window.
- risk_tier.
- approval_status.

### Risk assessment

Represents governance classification.

Key fields:

- assessment_id.
- request_id.
- data_risk_score.
- autonomy_risk_score.
- operational_risk_score.
- integration_risk_score.
- business_value_score.
- recommended_risk_tier.
- required_approvers.
- blocked_dependencies.
- rationale.

### Agent workflow trace

Represents an agent execution path.

Key fields:

- session_id.
- workflow_id.
- agent_id.
- tool_call_id.
- prompt_version.
- model_version.
- input_summary.
- output_summary.
- token_estimate.
- cost_estimate.
- latency_ms.
- approval_status.
- rollback_status.
- policy_decision.

### Integration contract

Represents a retail system API boundary.

Key fields:

- system_name.
- owner_team.
- api_name.
- purpose.
- data_classification.
- auth_requirement.
- allowed_operations.
- forbidden_operations.
- logging_requirement.
- SLA.
- rollback_notes.

## Design constraints

- AI does not become a system of record.
- AI recommendations must be traceable to inputs, prompt version, model version, and tool calls.
- High-risk and restricted actions require explicit approval.
- Payment data and sensitive customer data trigger elevated review.
- Autonomous action is disallowed for the initial replenishment workflow.
- The first production-shaped deployment should favor speed and simplicity before platform complexity.

## Recommended initial deployment pattern

For an interview demo, start with **Cloud Run-style architecture** rather than full GKE.

Rationale:

- Faster to deploy and iterate.
- Lower operational overhead.
- Natural fit for API services and event-driven AI workflows.
- Easier to explain cost controls and scaling.
- Can transition to GKE later if workflows require advanced orchestration, sidecars, service mesh, or more complex runtime isolation.

## Demo success criteria

A successful demo should show:

1. A business user submitting an AI request.
2. The platform classifying risk and dependencies.
3. The governance lead reviewing the request.
4. The architect seeing impacted retail systems and recommended integration patterns.
5. The agent workflow generating a replenishment recommendation.
6. The platform blocking execution until approval.
7. Trace/cost/latency metadata captured for the workflow.
8. SOP/runbook handoff documents available for IT support.
