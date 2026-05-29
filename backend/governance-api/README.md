# Phase 2 — Backend Governance API & Risk-Tiering Engine

This backend provides the API layer for the Family Dollar AI Governance & Agentic Workflow Platform.

## Purpose

The service evaluates AI intake requests, assigns preliminary risk tiers, stores submitted requests in memory for demo purposes, exposes governance dashboard metrics, and creates the backend foundation for future policy gates, retail API integration, agent workflow tracing, and deployment controls.

## Role Alignment

This phase demonstrates the AI Solutions Architect and Governance Lead responsibilities:

- Translate business requirements into API-backed solution candidates.
- Classify AI use cases by data sensitivity, autonomy, operational impact, and dependencies.
- Support governance intake and triage workflows.
- Prepare each request for architecture review, release planning, and support handoff.
- Build production-style backend code with schemas, routers, tests, and clear API contracts.

## Local Development

```bash
cd backend/governance-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Validation
cd backend/governance-api
pytest
Key Endpoints
Method	Path	Purpose
GET	/health	Service health
GET	/v1/risk/tiers	Risk-tier definitions
POST	/v1/intake/evaluate	Evaluate a request without storing it
POST	/v1/intake/requests	Submit and store an AI request
GET	/v1/intake/requests	List stored AI requests
GET	/v1/intake/requests/{request_id}	Get one AI request
GET	/v1/governance/dashboard	Governance portfolio metrics
Governance Principle

The engine provides a preliminary risk recommendation. It does not replace the governance forum, legal review, security review, architecture review, or executive approval for restricted use cases.
