# Phase 8 — Docker, Terraform, CI/CD & Deployment Readiness

## Summary

Phase 8 adds deployment-readiness scaffolding to the Family Dollar AI Governance & Agentic Workflow Platform.

This phase includes backend and frontend Dockerfiles, a local Docker Compose stack, GitHub Actions CI, and Terraform scaffolding for GCP Cloud Run.

## Why This Matters

The AI Solutions Architect and Governance Lead role requires building, testing, deploying, operating, and transitioning AI applications. This phase demonstrates delivery discipline and readiness for Google Cloud Platform deployment.

## Artifacts Added

### Docker

- `backend/governance-api/Dockerfile`
- `backend/governance-api/.dockerignore`
- `frontend/intake-portal/Dockerfile`
- `frontend/intake-portal/.dockerignore`
- `frontend/intake-portal/nginx.conf`
- `docker-compose.yml`

### CI/CD

- `.github/workflows/ci.yml`

### Terraform

- `infra/terraform/gcp-cloud-run/versions.tf`
- `infra/terraform/gcp-cloud-run/variables.tf`
- `infra/terraform/gcp-cloud-run/main.tf`
- `infra/terraform/gcp-cloud-run/outputs.tf`
- `infra/terraform/gcp-cloud-run/README.md`

## Local Validation

```bash
docker compose build
docker compose up

Expected local endpoints:

Frontend: http://localhost:8080
Backend health: http://localhost:8000/health
Backend docs: http://localhost:8000/docs
CI Validation

GitHub Actions validates:

Backend Python dependency install
Backend compile
Backend pytest
Frontend dependency install
Frontend production build
Backend Docker image build
Frontend Docker image build
Deployment Readiness

The Terraform scaffold shows a GCP Cloud Run deployment pattern for:

Governance API
Intake Portal

Actual production deployment would require:

Approved container registry
Service account design
IAM review
Secret management
Network controls
Observability
Rollback plan
Change ticket
Governance approval
Production readiness review
Demo Talk Track

"After building the platform capabilities, I added deployment-readiness scaffolding. The backend and frontend are containerized, the local stack runs through Docker Compose, CI validates tests and builds, and Terraform shows how the services could be deployed to GCP Cloud Run. I intentionally separated deployment readiness from production deployment because governed release requires change control, rollback, IAM, observability, and owner approval."

Likely Interview Questions
How would you containerize the platform?
How would you run the stack locally?
What should CI validate before merge?
Why Cloud Run versus GKE for this demo?
How would you promote from dev to test to prod?
What deployment controls would be required before production?
How would rollback work?
How would you manage secrets and IAM?
How would you connect this to Artifact Registry and Cloud Build?
How would you explain this deployment model to infrastructure and security teams?
Governance Principle

Deployment readiness is not production authorization. Production release requires governance approval, policy gates, change control, rollback, observability, and support handoff.
