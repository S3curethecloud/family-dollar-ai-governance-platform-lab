# API Endpoint Inventory

Status: Backend Review Baseline

## Purpose

Map the governance API endpoint surface before making backend changes.

## Backend Root

```text
backend/governance-api/
Primary API File
backend/governance-api/app/main.py
Test Suite
backend/governance-api/tests/
Known Review Areas
Governance intake endpoints
Risk tiering endpoints
Retail system API simulation endpoints
Inventory agent endpoints
Policy gate endpoints
Observability endpoints
Cost dashboard endpoints
Runbook/support handoff endpoints
Health/readiness endpoints
Review Boundary
Review only.
No backend code changes in this phase.
No API contract changes in this phase.
No policy logic changes in this phase.
No production enforcement changes in this phase.

