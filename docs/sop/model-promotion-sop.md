# Model Promotion SOP

## Purpose

This SOP defines how model versions are evaluated and promoted across environments.

## Scope

Applies to model changes for:

- RAG assistants
- Agentic workflows
- Document intelligence
- Forecasting
- Classification
- Generative AI personalization

## Required Metadata

- Model name
- Model version
- Workflow using the model
- Prompt version
- Risk tier
- Evaluation result
- Cost profile
- Latency profile
- Safety assessment
- Rollback model version

## Promotion Environments

| Environment | Purpose |
|---|---|
| Dev | Build and prototype |
| Test | Integration and governance validation |
| Prod | Controlled production release |

## Promotion Requirements

- Tests passed
- Evaluation completed
- Risk tier confirmed
- Prompt version approved
- Cost threshold reviewed
- Observability enabled
- Rollback plan present
- Owner approval present
- Governance review complete for Tier 3/Tier 4

## Procedure

1. Register candidate model version.
2. Run evaluation suite.
3. Compare output quality, safety, latency, and cost.
4. Run deployment gate.
5. Run environment promotion gate.
6. Obtain required approvals.
7. Promote to next environment.
8. Monitor post-promotion telemetry.
9. Record promotion evidence.

## Governance Principle

Model promotion is controlled change management. No model should move toward production without evaluation, observability, rollback, and approval evidence.
