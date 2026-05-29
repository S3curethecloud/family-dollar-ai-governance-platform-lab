from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_policy_gates_endpoint_lists_controls():
    response = client.get("/v1/policies/gates")

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 5
    assert any(gate["gate_type"] == "prompt_approval" for gate in body["gates"])


def test_prompt_approval_denies_autonomous_payment_prompt():
    response = client.post(
        "/v1/policies/prompt-approval",
        json={
            "prompt_id": "dangerous-prompt",
            "prompt_text": "Create purchase orders automatically using payment data.",
            "risk_tier": "Tier 4",
            "includes_payment_data": True,
            "asks_for_autonomous_action": True,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["decision"] == "deny"
    assert body["allowed"] is False


def test_prompt_approval_routes_pii_to_review():
    response = client.post(
        "/v1/policies/prompt-approval",
        json={
            "prompt_id": "crm-support-prompt",
            "prompt_text": "Draft a customer support response from redacted case notes.",
            "risk_tier": "Tier 3",
            "includes_pii": True,
            "customer_facing_output": True,
        },
    )

    assert response.status_code == 200
    assert response.json()["decision"] == "review"


def test_deployment_gate_denies_missing_controls():
    response = client.post(
        "/v1/policies/deployment-gate",
        json={
            "service_name": "inventory-agent",
            "environment": "prod",
            "risk_tier": "Tier 3",
            "tests_passed": True,
            "rollback_plan_present": False,
            "observability_enabled": False,
        },
    )

    assert response.status_code == 200
    assert response.json()["decision"] == "deny"


def test_action_gate_blocks_autonomous_execution():
    response = client.post(
        "/v1/policies/action-gate",
        json={
            "action_name": "create_purchase_order",
            "retail_system": "Inventory",
            "action_type": "autonomous_execution",
            "risk_tier": "Tier 4",
            "human_approval_status": "approved",
            "mutates_retail_system": True,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["decision"] == "deny"
    assert body["allowed"] is False


def test_environment_promotion_requires_change_controls():
    response = client.post(
        "/v1/policies/environment-promotion",
        json={
            "service_name": "inventory-agent",
            "from_environment": "dev",
            "to_environment": "test",
            "risk_tier": "Tier 2",
            "tests_passed": True,
            "change_ticket_present": False,
            "rollback_plan_present": True,
            "owner_approval_present": True,
        },
    )

    assert response.status_code == 200
    assert response.json()["decision"] == "deny"


def test_human_approval_allows_controlled_handoff():
    response = client.post(
        "/v1/policies/human-approval",
        json={
            "workflow_id": "wf-inventory-demo",
            "requested_action": "handoff_reorder_recommendation",
            "approver_role": "Store Operations Approver",
            "approval_status": "approved",
            "risk_tier": "Tier 2",
            "autonomous_execution_requested": False,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["decision"] == "allow"
    assert body["allowed"] is True


def test_human_approval_blocks_autonomous_execution_even_after_approval():
    response = client.post(
        "/v1/policies/human-approval",
        json={
            "workflow_id": "wf-inventory-demo",
            "requested_action": "create_purchase_order",
            "approver_role": "Store Operations Approver",
            "approval_status": "approved",
            "risk_tier": "Tier 2",
            "autonomous_execution_requested": True,
        },
    )

    assert response.status_code == 200
    assert response.json()["decision"] == "deny"
