# Architecture Talk Track

## Architecture Summary

The platform is organized into five layers:

1. Business intake and governance workflow
2. Backend governance API and risk-tiering engine
3. Retail system integration and data contracts
4. Agentic workflow execution with approval gates
5. Observability, policy controls, deployment readiness, and support handoff

## Component Breakdown

| Layer | Components |
|---|---|
| Frontend | React/Vite intake portal |
| Backend | FastAPI governance API |
| Risk | Rules-based risk-tiering engine |
| Retail APIs | Mock POS, inventory, ERP, CRM, supply-chain, identity APIs |
| Agent | Inventory Replenishment Assistant |
| Policy | Prompt, deployment, action, environment, and approval gates |
| Observability | Trace, latency, token, cost, and guardrail dashboard |
| Deployment | Docker, Docker Compose, GitHub Actions, Terraform Cloud Run scaffold |
| Operations | SOPs, runbooks, rollback, incident escalation, support handoff |

## GCP Alignment

This demo maps naturally to Google Cloud Platform:

| Platform Need | GCP Mapping |
|---|---|
| Container runtime | Cloud Run |
| Container registry | Artifact Registry |
| CI/CD | Cloud Build or GitHub Actions |
| Logs | Cloud Logging |
| Metrics | Cloud Monitoring |
| Secrets | Secret Manager |
| Identity | IAM |
| Data warehouse | BigQuery |
| AI services | Vertex AI / Gemini |
| Workflow orchestration | Workflows / Cloud Tasks |
| API perimeter | API Gateway / Cloud Load Balancing |

## Why Cloud Run

Cloud Run is appropriate for this demo because:

- Backend and frontend are containerized.
- Workloads are stateless.
- Scaling can be managed per service.
- Operational overhead is lower than GKE.
- It supports iterative delivery.
- It aligns with fast prototyping and controlled rollout.

## When GKE Would Be Considered

GKE may be more appropriate if:

- Long-running workers are required.
- Complex service mesh policies are required.
- Fine-grained Kubernetes admission control is required.
- Multi-service orchestration becomes more complex.
- Platform teams already standardize on GKE.

## Governance Boundary

Deployment readiness is not production authorization. Production release still requires policy gates, IAM review, secrets review, change control, rollback, observability, and support handoff.
