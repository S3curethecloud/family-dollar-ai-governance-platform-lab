# GCP Cloud Run Terraform Scaffold

## Purpose

This Terraform scaffold shows how the Family Dollar AI Governance & Agentic Workflow Platform could be deployed to Google Cloud Run.

It is intentionally deployment-readiness scaffolding. Do not run `terraform apply` unless you intend to create cloud resources.

## Services

- `family-dollar-governance-api`
- `family-dollar-intake-portal`

## Required Variables

- `project_id`
- `region`
- `backend_image`
- `frontend_image`
- `environment`

## Example Plan Command

```bash
terraform init
terraform plan \
  -var="project_id=YOUR_PROJECT_ID" \
  -var="region=us-central1" \
  -var="backend_image=us-central1-docker.pkg.dev/YOUR_PROJECT/fd/governance-api:demo" \
  -var="frontend_image=us-central1-docker.pkg.dev/YOUR_PROJECT/fd/intake-portal:demo" \
  -var="environment=demo"
Governance Note

Production deployment requires policy-gate approval, rollback plan, observability, owner approval, change ticket, and environment-promotion review.
