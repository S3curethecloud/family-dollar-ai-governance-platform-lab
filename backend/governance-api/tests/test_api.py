from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_risk_tiers_endpoint():
    response = client.get("/v1/risk/tiers")

    assert response.status_code == 200
    assert len(response.json()) == 4


def test_governance_dashboard_endpoint():
    response = client.get("/v1/governance/dashboard")

    assert response.status_code == 200
    body = response.json()
    assert body["total_requests"] >= 3
    assert "portfolio_risk_posture" in body


def test_evaluate_request_endpoint():
    payload = {
        "business_unit": "Store Operations",
        "requester": "Regional Operations Director",
        "use_case": "Inventory Replenishment Assistant",
        "retail_system": "Inventory",
        "data_sensitivity": "Internal",
        "customer_data": False,
        "payment_data": False,
        "operational_impact": "Store-level operations",
        "expected_business_value": "Reduce stockouts and improve shelf availability.",
        "model_type": "Agentic workflow with retrieval",
        "autonomous_action_level": "Recommend only",
        "human_approval_required": True,
        "dependencies": ["Inventory API", "Supply Chain API"],
        "target_release_window": "Q3 pilot",
    }

    response = client.post("/v1/intake/evaluate", json=payload)

    assert response.status_code == 200
    assert response.json()["risk_tier"] == "Tier 2"


def test_submit_request_endpoint():
    payload = {
        "business_unit": "Finance",
        "requester": "Finance Shared Services",
        "use_case": "Invoice Exception Summarizer",
        "retail_system": "ERP",
        "data_sensitivity": "Confidential",
        "customer_data": False,
        "payment_data": False,
        "operational_impact": "Back-office operations",
        "expected_business_value": "Reduce manual review time for invoice exceptions.",
        "model_type": "Document intelligence",
        "autonomous_action_level": "Recommend only",
        "human_approval_required": True,
        "dependencies": ["ERP API", "Finance approval queue"],
        "target_release_window": "Q3 prototype",
    }

    response = client.post("/v1/intake/requests", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["request"]["request_id"].startswith("FD-AI-")
    assert body["request"]["evaluation"]["risk_tier"] in [
        "Tier 1",
        "Tier 2",
        "Tier 3",
        "Tier 4",
    ]
