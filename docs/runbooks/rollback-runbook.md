# Rollback Runbook

## Purpose

This runbook defines how to roll back an AI workflow, prompt, model version, or deployment when safety, quality, cost, or operational controls fail.

## Rollback Triggers

- Failed deployment validation
- Failed policy gate
- Excessive cost or token usage
- Unsafe model output
- Incorrect recommendation
- Missing trace events
- Missing approval record
- Customer-impacting issue
- Retail-system mutation outside approved handoff
- Incident declared by IT, security, or governance

## Rollback Scope

Rollback may apply to:

- Prompt version
- Model version
- Agent workflow version
- API service release
- Policy configuration
- Environment promotion
- Support handoff state

## Procedure

1. Declare rollback condition.
2. Identify affected service, workflow, prompt, or model version.
3. Freeze new workflow executions.
4. Route active workflows to manual review.
5. Revert to the last approved version.
6. Validate health check.
7. Validate policy gates.
8. Validate observability dashboard.
9. Notify governance forum and support owner.
10. Record rollback evidence.

## Required Evidence

- Incident or change ticket
- Failed validation output
- Affected workflow ID
- Affected prompt/model version
- Rollback commit or release ID
- Post-rollback validation result
- Owner approval
- Governance review note

## Governance Principle

Rollback must preserve auditability. A rollback is not complete until evidence, owner approval, and post-rollback validation are recorded.
