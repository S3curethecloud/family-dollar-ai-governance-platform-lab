# Prompt Versioning SOP

## Purpose

This SOP defines how prompts are versioned, reviewed, approved, and rolled back.

## Prompt Version Format

Use semantic and workflow-specific naming:

```text
<workflow>-prompt-v<major>.<minor>

Example:

inventory-agent-prompt-v0.4
Required Metadata
Prompt ID
Prompt text
Workflow owner
Risk tier
Model version
Intended use
Data sensitivity
Customer-facing status
PII/payment-data status
Approval status
Rollback version
Approval Requirements

Prompt review is required when:

Prompt includes PII.
Prompt includes payment data.
Prompt creates customer-facing output.
Prompt requests autonomous action.
Prompt is used in Tier 3 or Tier 4 workflow.
Prompt materially changes agent behavior.
Procedure
Draft prompt update.
Record prompt ID and version.
Run prompt approval gate.
Review deny/review/allow decision.
Complete required privacy/security/governance review.
Run test workflow.
Record validation evidence.
Promote prompt only after approval.
Rollback

Rollback prompt if:

Output quality degrades.
Safety issue is detected.
Prompt creates unauthorized action request.
PII/payment-data boundary fails.
Governance approval is missing.
Governance Principle

Prompts are production artifacts. They must be versioned, reviewed, tested, and auditable like code.
