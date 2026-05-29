# Risk Tiering Runbook

## Purpose

This runbook explains how AI use cases are classified into governance risk tiers.

## Risk Tiers

| Tier | Label | Meaning |
|---|---|---|
| Tier 1 | Low Risk | Internal productivity, low sensitivity, no operational execution |
| Tier 2 | Moderate Risk | Business workflow support with human approval |
| Tier 3 | High Risk | Customer data, sensitive output, customer-facing impact |
| Tier 4 | Restricted | Payment data, autonomous action, executive review, or regulated impact |

## Risk Inputs

- Data sensitivity
- Customer data involvement
- Payment data involvement
- Operational impact
- Autonomous action level
- Dependency count
- Human approval requirement

## Required Reviews

| Trigger | Required Review |
|---|---|
| Customer data | Privacy Review, Security Review |
| Payment data | PCI Review, Executive Review |
| Autonomous action | AI Governance Forum, Executive Review |
| Confidential data | Data Governance Review |
| Supply-chain or enterprise-critical impact | Operational Resilience Review |

## Procedure

1. Retrieve the intake request.
2. Review the preliminary risk score and tier.
3. Inspect rationale and blocked reasons.
4. Confirm whether required reviews are complete.
5. Assign owner team.
6. Set governance status.
7. Communicate next step to requester.

## Escalation

Escalate to the AI Governance Forum when:

- Request is Tier 3 or Tier 4.
- Payment data is involved.
- Autonomous execution is requested.
- Customer-facing output is generated.
- Dependencies cross multiple enterprise systems.
- Legal, security, privacy, or compliance review is unclear.

## Governance Principle

The risk engine provides a preliminary recommendation. Final approval remains with the governance forum, security, privacy, architecture, and executive reviewers where applicable.
