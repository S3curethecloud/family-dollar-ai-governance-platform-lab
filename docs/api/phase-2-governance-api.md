
Phase 2 — Backend Governance API & Risk-Tiering Engine
Summary

Phase 2 adds the backend service for the Family Dollar AI Governance & Agentic Workflow Platform.

The API evaluates AI intake requests, assigns preliminary risk tiers, stores demo requests, and exposes dashboard metrics for governance forum review.

Why This Matters for the Interview

This shows that the platform is not only a UI. It has a backend decision layer that can receive business requirements, evaluate risk, expose structured API contracts, and support delivery governance.

API Capabilities
Health check
Risk tier definitions
Request evaluation
Request submission
Request listing
Request lookup
Governance dashboard metrics
Risk Inputs
Data sensitivity
Customer data involvement
Payment data involvement
Operational impact
Autonomous action level
Dependency count
Human approval requirement
Risk Outputs
Risk tier
Risk score
Governance status
Owner team
Required reviews
Blocked reasons
Risk rationale
Recommended next step
Demo Talk Track

"I added a backend governance API because intake should not just be a static form. The API accepts structured AI requests, evaluates risk using transparent rules, returns required reviews and blocked reasons, and exposes portfolio metrics for the governance forum. This is the foundation for integrating Jira, ServiceNow, GitHub Actions, GCP deployment gates, and policy-as-code in later phases."

Likely Interview Questions
How would you classify AI use cases into risk tiers?
How would you ensure the risk decision is explainable?
How would the frontend intake portal integrate with backend governance workflows?
What would trigger executive review?
How would you prevent autonomous AI from taking operational action?
How would this API later integrate with ServiceNow, Jira, or GitHub Actions?
How would you evolve this from in-memory demo storage to production persistence?
What would you log for auditability?
How would this support change control and release governance?
How would you explain this architecture to security and infrastructure teams?
