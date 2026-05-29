# Demo Checklist

## Before the Interview

- [ ] Pull latest `main`
- [ ] Confirm Docker Desktop is running
- [ ] Confirm backend tests pass
- [ ] Confirm frontend builds
- [ ] Confirm Docker Compose builds
- [ ] Confirm backend health endpoint works
- [ ] Confirm frontend health endpoint works
- [ ] Open GitHub repo in browser
- [ ] Open README
- [ ] Open architecture docs
- [ ] Open pull request history
- [ ] Open terminal with repo ready
- [ ] Have five-minute script ready

## Commands to Validate

```bash
cd ~/family-dollar-ai-governance-platform-lab

docker compose build
docker compose up

In another terminal:

curl http://localhost:8000/health
curl http://localhost:8000/v1/risk/tiers
curl http://localhost:8000/v1/retail/systems
curl http://localhost:8000/v1/policies/gates
curl http://localhost:8000/v1/observability/dashboard
curl http://localhost:8080/health
Demo Flow
Show README and roadmap.
Show intake portal.
Show backend API docs or curl output.
Show retail data contracts.
Run inventory agent workflow.
Approve workflow and show autonomous execution remains blocked.
Show policy gate denying autonomous purchase order.
Show observability dashboard.
Show Docker/Terraform/CI.
Show SOPs and handoff docs.
Key Phrases
"Governance starts at intake."
"AI integrates through governed APIs, not shadow access."
"The agent can recommend, but cannot execute."
"Policy gates make governance enforceable."
"Observability proves the workflow stayed inside boundaries."
"Support handoff requires evidence, not trust."
