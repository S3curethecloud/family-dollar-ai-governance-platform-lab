# AI Governance Operating Model

## Purpose

This operating model defines how the platform receives AI requests, evaluates risk, prioritizes delivery, manages dependencies, communicates release windows, governs changes, and transitions AI applications to IT support.

The model is designed for a role that combines hands-on AI solution architecture with governance forum ownership.

## Governance objectives

- Accelerate safe AI delivery.
- Make risk visible early.
- Map business value to delivery priority.
- Identify impacted systems and owners before buildout.
- Prevent uncontrolled AI access to sensitive retail systems.
- Require approval for high-risk or operationally impactful workflows.
- Track release windows, dependencies, and post-implementation reviews.
- Ensure every AI application has an operating model before production use.

## Governance lifecycle

```text
1. Intake
2. Completeness review
3. Risk tiering
4. Dependency mapping
5. Architecture recommendation
6. Governance forum review
7. Prototype approval
8. Build and test
9. Deployment readiness review
10. Release window approval
11. Production or demo deployment
12. Monitoring and support handoff
13. Post-implementation review
```

## Request states

| State | Meaning |
|---|---|
| Draft | Request is being prepared by the business user |
| Submitted | Request has entered governance intake |
| Needs Info | Required intake fields or business details are missing |
| Triage | Governance lead is reviewing business value, risk, and dependencies |
| Architecture Review | Architect is defining solution pattern and integrations |
| Security Review | Security/privacy concerns require review |
| Approved for Prototype | Request may move to hands-on build/prototype |
| Blocked | Dependency, risk, data, or ownership issue blocks progress |
| Approved for Release | Build passed readiness review and has release window |
| Released | Solution has been deployed to the approved environment |
| Handoff | IT support transition is in progress |
| Operational | Support model is active |
| PIR Required | Post-implementation review is pending |
| Closed | Request completed, rejected, or retired |

## Risk tier model

| Tier | Label | Description | Required governance path |
|---|---|---|---|
| Tier 1 | Low Risk | Internal productivity or read-only use with non-sensitive data | Fast-track review |
| Tier 2 | Moderate Risk | Internal operational data, limited business impact, no autonomous execution | Governance lead and system owner review |
| Tier 3 | High Risk | Customer impact, sensitive data, operational dependency, or approval-gated execution | Governance forum, security, system owner, and release readiness review |
| Tier 4 | Restricted / Executive Review | Payment data, employment impact, high autonomy, material financial or customer risk | Executive/security/legal review before prototype or deployment |

## Intake evaluation dimensions

| Dimension | Example questions |
|---|---|
| Business value | What problem does this solve? What is the measurable outcome? |
| Criticality | Would failure affect customers, stores, employees, or financial operations? |
| Data sensitivity | Does the workflow use PII, payment data, employee data, or confidential business data? |
| Retail systems touched | Which systems are read from or written to? |
| Autonomy | Does AI only summarize, recommend, route, or execute? |
| Human oversight | Who approves recommendations before execution? |
| Dependencies | Which application, data, platform, infrastructure, and security teams are required? |
| Release timing | Is there a release window, freeze period, peak retail season, or dependency window? |
| Support readiness | Is there a runbook, dashboard, alert, rollback plan, and escalation path? |

## Governance forum cadence

Recommended forum structure:

- **Weekly AI intake triage:** Review newly submitted requests, missing information, rough risk, and business value.
- **Biweekly architecture and dependency review:** Review integrations, platform needs, data access, security controls, and delivery plan.
- **Release readiness review:** Review test evidence, model/prompt versions, rollback, monitoring, support handoff, and approval state.
- **Monthly portfolio review:** Review request volume, risk trend, cost trend, blocked dependencies, post-implementation findings, and operating model health.

## Governance forum agenda

1. New intake requests.
2. Risk tier changes.
3. High-risk or restricted requests.
4. Blocked dependencies.
5. Prototype approvals.
6. Release windows.
7. Production readiness evidence.
8. Incidents or rollback events.
9. Post-implementation review findings.
10. Portfolio metrics and cost trend.

## Approval model

| Decision | Required approver |
|---|---|
| Tier 1 prototype | AI governance lead |
| Tier 2 prototype | AI governance lead + system owner |
| Tier 3 prototype | Governance forum + system owner + security representative |
| Tier 4 prototype | Executive/security/legal review |
| Operational write enablement | System owner + governance lead + security where applicable |
| Production release | Platform owner + support owner + governance lead |
| Emergency rollback | Incident commander or platform owner, with post-action review |

## Prompt and model governance

Each deployed AI workflow must track:

- prompt_name.
- prompt_version.
- model_name.
- model_version.
- evaluation_status.
- approval_status.
- owner.
- release_date.
- rollback_version.
- known limitations.

Prompt/model changes should be treated as change-controlled artifacts when they affect production behavior.

## Cost governance

The platform should track:

- token_estimate.
- cost_estimate.
- average latency.
- retries.
- failed tool calls.
- high-cost workflows.
- cost by business unit.
- cost by use case.

Cost controls include:

- model selection by risk and complexity.
- caching where appropriate.
- limiting agent tool loops.
- setting workflow step budgets.
- alerting on cost anomalies.
- reviewing cost trend in the governance forum.

## Support handoff criteria

A solution should not be considered operationally complete until the following exist:

- Named business owner.
- Named technical owner.
- Named support owner.
- Runbook.
- SOP.
- Dashboard.
- Alert policy.
- Incident escalation path.
- Rollback procedure.
- Prompt/model version record.
- Known limitations.
- Post-implementation review date.

## Post-implementation review

Each meaningful AI release should answer:

- Did the solution meet the intended business outcome?
- Were there unexpected model behaviors?
- Were governance controls sufficient?
- Did latency and cost stay within expected bounds?
- Were system integrations stable?
- Did support receive enough documentation?
- Should the solution be scaled, changed, paused, or retired?

## Interview talking points

- “Governance should not be a blocker; it should be a routing and acceleration mechanism.”
- “I would classify intake by value, risk, dependency, criticality, autonomy, and data sensitivity.”
- “I would maintain a governance forum dashboard so the business can see what is approved, blocked, released, or waiting for review.”
- “Prompt and model versions are release artifacts, not casual configuration.”
- “A solution is not finished until support has a runbook, dashboard, rollback path, and escalation model.”
