# Retail Integration Patterns

## Purpose

This document defines how AI applications in the demo platform integrate with existing retail systems without becoming uncontrolled shadow systems.

The platform assumes that Family Dollar-style retail operations depend on multiple systems of record, including POS, inventory, ERP, CRM, supply chain, identity, store operations, and IT support platforms. AI workflows may read, summarize, recommend, and route approvals, but operational writes must be controlled by policy, system ownership, and human approval.

## Integration principles

1. **System owners remain accountable.** The AI platform does not own POS, ERP, CRM, inventory, or supply-chain systems.
2. **AI reads through approved APIs.** Direct database access is avoided unless explicitly approved and governed.
3. **Writes require stricter control than reads.** Any operational write requires approval, audit, and rollback planning.
4. **AI recommendations are not execution authority.** A recommendation must pass policy and approval before execution.
5. **Data contracts define trust boundaries.** Each API contract must identify data sensitivity, owner, SLA, auth, logging, and allowed operations.
6. **Retail operations need fail-safe behavior.** If AI, policy, or approval state is unavailable, the workflow fails closed.

## System integration matrix

| System | Typical AI use | Initial access mode | Risk notes | Owner dependency |
|---|---|---|---|---|
| POS | Sales trends, transaction summaries, demand signals | Read-only mock API | Payment and customer data risk | POS application owner, security |
| Inventory | Stock levels, replenishment candidates, shrink signals | Read-only plus approval-gated recommendation | Store operations impact | Inventory application owner |
| ERP | Purchase orders, finance, vendor records | Read-only in demo | Financial and operational dependency risk | ERP owner, finance, security |
| CRM | Customer context, support trends, loyalty insights | Restricted read-only | PII and customer impact | CRM owner, privacy/security |
| Supply Chain | Shipment status, vendor delays, distribution center capacity | Read-only plus recommendation | Operational and supplier dependency risk | Supply-chain systems owner |
| Identity | User, role, approver, business unit | Read-only role lookup | Access control and audit risk | IAM/platform/security |
| Store Operations | Task assignment, incident notes, manager approvals | Approval-gated workflow | Store execution risk | Store operations owner |
| IT Support | Handoff, incident routing, operational support | Ticket creation after approval | Support readiness risk | IT service management owner |

## API/data contract standard

Each integration contract should include:

```yaml
system_name: inventory
api_name: Inventory Availability API
owner_team: Retail Inventory Systems
data_classification: internal_operational
auth_requirement: service_account_with_least_privilege
allowed_operations:
  - read_store_inventory
  - read_sku_availability
  - read_replenishment_thresholds
forbidden_operations:
  - autonomous_purchase_order_creation
  - inventory_quantity_mutation_without_source_system
logging_requirement:
  - request_id
  - user_or_service_identity
  - timestamp
  - purpose
  - records_accessed
  - policy_decision
sla: 99.5% for read availability in production
rollback_notes: no direct write operation in initial AI workflow
risk_classification: moderate
```

## Read-only pattern

Use this pattern for early AI use cases where the model summarizes, ranks, classifies, or recommends.

```text
AI Workflow -> API Gateway / Service Boundary -> Retail System API -> Response -> AI Recommendation -> Human Review
```

Controls:

- API authentication.
- Field-level minimization.
- Request purpose logging.
- Model/prompt version logging.
- No write operation.
- Risk-tier-based review.

Best fit:

- Store performance summaries.
- Inventory risk summaries.
- Support ticket summarization.
- Vendor delay summarization.
- Knowledge assistant workflows.

## Approval-gated write pattern

Use this pattern when AI generates an operational recommendation that could later become an action.

```text
AI Workflow
  -> Recommendation
  -> Policy Gate
  -> Human Approval
  -> System Owner API
  -> Audit Log
  -> Rollback/Compensation Plan
```

Controls:

- Risk tier must permit the operation.
- Human approval must be recorded.
- Approver must have the correct role.
- Execution request must include source trace IDs.
- Rollback or compensation process must exist.
- Post-implementation review must be scheduled for higher-risk releases.

Best fit:

- Replenishment recommendations.
- Store task creation.
- Support ticket routing.
- Promotion planning suggestions.

## Restricted pattern

Use this pattern when the AI use case involves payment data, sensitive customer data, employment impact, high operational autonomy, or material financial exposure.

```text
Intake -> Tier 4 Classification -> Executive/Security/Legal Review -> Architecture Exception Board -> Approved Pilot Only
```

Controls:

- No direct production execution in the demo.
- Executive or delegated governance approval.
- Privacy/security review.
- Data minimization plan.
- Model evaluation plan.
- Explicit rollback and incident response plan.

Best fit:

- Payment data analysis.
- Customer-specific automated decisions.
- Employment-impacting workflows.
- Fully autonomous supply-chain actions.

## Inventory replenishment assistant integration pattern

Initial workflow:

1. Read store inventory.
2. Read SKU demand signals.
3. Read supply-chain delay indicators.
4. Compute low-stock risk.
5. Generate recommendation.
6. Route to human approval.
7. Do not execute reorder in Phase 4.

The workflow intentionally stops before order execution. This demonstrates safe architecture judgment and governance control.

## Integration anti-patterns

Avoid these patterns:

- AI service directly querying production databases without an approved contract.
- AI agent holding broad credentials to multiple systems.
- Prompt instructions used as the only control layer.
- Model output used as an authorization decision.
- Autonomous writes to inventory, ERP, POS, or CRM without approval.
- No traceability from recommendation to data source, prompt version, model version, and policy decision.
- No rollback or support handoff before production release.

## Interview talking points

Use these concise explanations during the interview:

- “I would treat AI as an orchestration and recommendation layer, not as a new system of record.”
- “Each retail integration needs an owner, contract, auth boundary, data classification, SLA, and logging requirement.”
- “For early delivery, I would bias toward read-only integrations and approval-gated writes.”
- “The agent can recommend a reorder, but execution requires policy and human approval.”
- “Every recommendation should be traceable back to data inputs, prompt version, model version, and tool calls.”
