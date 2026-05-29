from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_observability_dashboard_returns_trace_and_cost_summary():
    response = client.get("/v1/observability/dashboard")

    assert response.status_code == 200
    body = response.json()
    assert body["total_workflows"] == 1
    assert body["total_trace_events"] >= 6
    assert body["total_token_estimate"] > 0
    assert body["total_cost_estimate_usd"] > 0
    assert body["portfolio_status"] == "healthy"


def test_observability_dashboard_tracks_autonomous_execution_boundary():
    response = client.get("/v1/observability/dashboard")

    assert response.status_code == 200
    body = response.json()
    assert body["blocked_autonomous_actions"] == 1
    assert body["trace_summaries"][0]["autonomous_execution_allowed"] is False
    assert body["trace_summaries"][0]["human_approval_required"] is True


def test_observability_dashboard_contains_guardrails():
    response = client.get("/v1/observability/dashboard")

    assert response.status_code == 200
    body = response.json()
    guardrail_names = [guardrail["name"] for guardrail in body["guardrails"]]

    assert "Autonomous Execution Guardrail" in guardrail_names
    assert "Cost Guardrail" in guardrail_names
    assert "Latency Guardrail" in guardrail_names
    assert "Human Approval Guardrail" in guardrail_names


def test_cost_guardrail_allows_low_cost_workflow():
    response = client.post(
        "/v1/observability/cost-guardrail",
        json={
            "workflow_id": "wf-low-cost",
            "estimated_tokens": 1200,
            "estimated_cost_usd": 0.0025,
            "max_tokens": 5000,
            "max_cost_usd": 0.05,
            "risk_tier": "Tier 2",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["allowed"] is True
    assert body["status"] == "healthy"


def test_cost_guardrail_blocks_expensive_workflow():
    response = client.post(
        "/v1/observability/cost-guardrail",
        json={
            "workflow_id": "wf-expensive",
            "estimated_tokens": 12000,
            "estimated_cost_usd": 0.12,
            "max_tokens": 5000,
            "max_cost_usd": 0.05,
            "risk_tier": "Tier 2",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["allowed"] is False
    assert body["status"] == "warning"
    assert len(body["required_actions"]) >= 1


def test_cost_guardrail_routes_high_risk_cost_to_review():
    response = client.post(
        "/v1/observability/cost-guardrail",
        json={
            "workflow_id": "wf-high-risk-cost",
            "estimated_tokens": 3000,
            "estimated_cost_usd": 0.03,
            "max_tokens": 5000,
            "max_cost_usd": 0.05,
            "risk_tier": "Tier 3",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["allowed"] is False
    assert "High-risk workflow exceeds half of cost threshold." in body["reasons"]
