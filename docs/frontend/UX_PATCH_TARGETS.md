
UX Patch Targets

Status: Patch Target Baseline

Purpose

Define likely frontend UX patch targets after source inspection.

Likely Patch Areas
Executive summary clarity
Card hierarchy
Grid spacing
Risk tier readability
Policy gate status readability
Agent workflow scanability
Enterprise system/API ownership clarity
Observability/cost visibility
Runbook/support handoff visibility
Mobile overflow hardening
Small-screen card stacking
Dense list readability
Patch Rules
Patch only after source sections are mapped.
Preserve existing backend/API behavior.
Preserve existing data fixtures unless explicitly scoped.
Do not change policy decisions.
Do not claim production enforcement.
Prefer visual hardening before feature expansion.
Validation Requirements
npm build or frontend build passes
No backend tests required unless backend contracts change
Git diff limited to scoped frontend assets
Manual screenshot review recommended
Mobile viewport review recommended

