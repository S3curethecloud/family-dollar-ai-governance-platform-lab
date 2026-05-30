
Policy Decision Map

Status: Policy Review Baseline

Purpose

Map policy files to governance decision categories before any policy mutation.

Decision Categories
ALLOW
DENY
REQUIRES_APPROVAL
REQUIRES_HUMAN_REVIEW
REQUIRES_PROMOTION_CONTROL
REQUIRES_DEPLOYMENT_GATE
Policy-to-Decision Mapping
action-gates.rego
  - governs whether AI or agent actions are allowed, blocked, or approval-bound

deployment-gates.rego
  - governs whether deployment activity can proceed

environment-promotion.rego
  - governs whether artifacts or workflows may move between environments

human-approval.rego
  - governs whether human approval is required before action execution

prompt-approval.rego
  - governs prompt governance and approval requirements
Governance Meaning
Policy gates convert governance requirements into deterministic decision points.
They help explain whether an AI workflow may proceed, must be blocked, or requires approval.
Review Boundary
Review only.
No policy decision changes.
No production enforcement claims.

