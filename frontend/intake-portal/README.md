# Phase 1 — Governance Intake Portal

This frontend demonstrates the intake UI/UX layer for the Family Dollar AI Governance & Agentic Workflow Platform.

## Purpose

The intake portal captures business AI requests, maps them to retail systems, previews governance risk, exposes dependencies, and prepares each use case for architecture review and governance forum triage.

## Role Alignment

This phase maps directly to the AI Solutions Architect and Governance Lead responsibilities:

- Maintain the AI intake UI/UX.
- Translate business requirements into solution candidates.
- Map requests to risk tiers and dependencies.
- Triage based on business value, criticality, risk, and delivery readiness.
- Communicate release windows and governance status.
- Create a repeatable operating model for AI delivery.

## Demo Flow

1. Open the portal.
2. Review the governance dashboard summary.
3. Submit a new AI use case.
4. Show the automated risk preview.
5. Explain that risk preview is an intake accelerator, not the final governance decision.
6. Show the request entering the governance queue.
7. Explain that future phases add backend persistence, policy gates, retail integration contracts, agent tracing, and deployment controls.

## Local Development

```bash
cd frontend/intake-portal
npm install
npm run dev
Production Build
cd frontend/intake-portal
npm run build
Governance Principle

AI may recommend, summarize, or draft. Human or policy approval is required before operational execution, customer-impacting action, payment-related action, or restricted release.
