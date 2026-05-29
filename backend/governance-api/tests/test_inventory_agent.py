from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_inventory_agent_run_is_approval_gated():
    response = client.post(
        "/v1/agents/inventory-replenishment/run",
        json={
            "requested_by": "test-ai-platform",
            "store_ids": ["STORE-1042", "STORE-2210"],
            "business_goal": "Identify low-stock inventory risk.",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["workflow_status"] == "awaiting_approval"
    assert body["approval_status"] == "required"
    assert body["human_approval_required"] is True
    assert body["autonomous_execution_allowed"] is False
    assert len(body["recommendations"]) >= 1


def test_inventory_agent_trace_contains_governed_tool_calls():
    response = client.post(
        "/v1/agents/inventory-replenishment/run",
        json={
            "requested_by": "test-ai-platform",
            "store_ids": ["STORE-1042"],
        },
    )

    assert response.status_code == 200
    body = response.json()
    step_names = [event["step_name"] for event in body["trace_events"]]

    assert "inspect_low_stock_inventory" in step_names
    assert "check_store_demand_signals" in step_names
    assert "generate_reorder_recommendations" in step_names
    assert "enforce_approval_gate" in step_names
    assert body["total_token_estimate"] > 0
    assert body["total_cost_estimate_usd"] > 0


def test_inventory_agent_workflow_lookup():
    run_response = client.post(
        "/v1/agents/inventory-replenishment/run",
        json={
            "requested_by": "test-ai-platform",
            "store_ids": ["STORE-1042"],
        },
    )

    workflow_id = run_response.json()["workflow_id"]

    lookup_response = client.get(
        f"/v1/agents/inventory-replenishment/workflows/{workflow_id}"
    )

    assert lookup_response.status_code == 200
    assert lookup_response.json()["workflow_id"] == workflow_id


def test_inventory_agent_approval_keeps_autonomous_execution_blocked():
    run_response = client.post(
        "/v1/agents/inventory-replenishment/run",
        json={
            "requested_by": "test-ai-platform",
            "store_ids": ["STORE-1042"],
        },
    )

    workflow_id = run_response.json()["workflow_id"]

    approval_response = client.post(
        "/v1/agents/inventory-replenishment/approval",
        json={
            "workflow_id": workflow_id,
            "approved_by": "store-manager-1042",
            "decision": "approve",
            "approval_note": "Approved for controlled handoff.",
        },
    )

    assert approval_response.status_code == 200
    body = approval_response.json()
    assert body["approval_status"] == "approved"
    assert body["workflow_status"] == "approved_for_handoff"
    assert body["handoff_ready"] is True
    assert body["autonomous_execution_allowed"] is False


def test_inventory_agent_rejection_blocks_handoff():
    run_response = client.post(
        "/v1/agents/inventory-replenishment/run",
        json={
            "requested_by": "test-ai-platform",
            "store_ids": ["STORE-1042"],
        },
    )

    workflow_id = run_response.json()["workflow_id"]

    rejection_response = client.post(
        "/v1/agents/inventory-replenishment/approval",
        json={
            "workflow_id": workflow_id,
            "approved_by": "store-manager-1042",
            "decision": "reject",
            "approval_note": "Supplier ETA requires manual review.",
        },
    )

    assert rejection_response.status_code == 200
    body = rejection_response.json()
    assert body["approval_status"] == "rejected"
    assert body["workflow_status"] == "rejected"
    assert body["handoff_ready"] is False
    assert body["autonomous_execution_allowed"] is False


def test_unknown_inventory_workflow_returns_404():
    response = client.get(
        "/v1/agents/inventory-replenishment/workflows/missing-workflow"
    )

    assert response.status_code == 404
