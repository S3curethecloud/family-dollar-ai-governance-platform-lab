# Runbooks and SOP Index

## Purpose

This directory will contain the operating procedures required to transition AI solutions from hands-on build to IT support.

The principle is simple:

> An AI solution is not operationally complete until support can monitor, triage, escalate, and roll back the solution using documented procedures.

## Planned runbooks

| Document | Purpose | Phase |
|---|---|---|
| AI Intake SOP.md | Defines how business AI requests are submitted, reviewed, and completed | Phase 7 |
| Risk Tiering Runbook.md | Defines how risk tiers are assigned, reviewed, overridden, and audited | Phase 7 |
| Agent Deployment Runbook.md | Defines deployment steps for governed AI workflows | Phase 7 |
| Rollback Runbook.md | Defines rollback triggers and rollback execution steps | Phase 7 |
| Incident Escalation Runbook.md | Defines AI incident severity, escalation, and communications | Phase 7 |
| Prompt Versioning SOP.md | Defines prompt ownership, approval, release, and rollback | Phase 7 |
| Model Promotion SOP.md | Defines model evaluation, approval, and environment promotion | Phase 7 |
| Support Handoff Checklist.md | Defines minimum handoff requirements before IT support accepts ownership | Phase 7 |
| Post-Implementation Review Template.md | Defines PIR review questions and evidence capture | Phase 7 |

## Minimum handoff requirements

Every AI application must have:

- Business owner.
- Technical owner.
- Support owner.
- Risk tier.
- Current prompt version.
- Current model version.
- Data sources.
- API dependencies.
- Dashboard link or telemetry view.
- Alerting rules.
- Known limitations.
- Rollback procedure.
- Incident escalation path.
- Post-implementation review date.

## Interview talking point

Use this phrase:

> I do not treat handoff as an afterthought. I design the operating model while I design the solution, so support, rollback, observability, and escalation are ready before production release.
