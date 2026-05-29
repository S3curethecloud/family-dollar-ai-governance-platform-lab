from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_retail_systems_endpoint_returns_contracts():
    response = client.get("/v1/retail/systems")

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 6
    assert any(system["system_id"] == "inventory" for system in body["systems"])


def test_inventory_contract_contains_human_approval_boundary():
    response = client.get("/v1/retail/contracts/inventory")

    assert response.status_code == 200
    contract = response.json()["contract"]
    assert contract["owner_team"] == "Inventory Platform"
    assert "Autonomously place purchase orders" in contract["forbidden_operations"]
    assert "Human approval" in contract["ai_usage_notes"]


def test_low_stock_inventory_endpoint():
    response = client.get("/v1/retail/inventory/low-stock")

    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 1
    assert body["items"][0]["on_hand_units"] < body["items"][0]["reorder_point"]


def test_reorder_recommendations_are_approval_gated():
    response = client.get("/v1/retail/inventory/reorder-recommendations")

    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 1
    assert body["recommendations"][0]["requires_human_approval"] is True
    assert body["recommendations"][0]["forbidden_autonomous_execution"] is True


def test_pos_sales_summary_endpoint():
    response = client.get("/v1/retail/pos/stores/STORE-1042/sales-summary")

    assert response.status_code == 200
    body = response.json()
    assert body["store_id"] == "STORE-1042"
    assert body["transaction_count"] > 0


def test_crm_context_is_redacted():
    response = client.get("/v1/retail/crm/cases/CASE-9001/support-context")

    assert response.status_code == 200
    body = response.json()
    assert body["pii_redacted"] is True


def test_identity_subject_access_context():
    response = client.get("/v1/retail/identity/subjects/user-store-manager")

    assert response.status_code == 200
    body = response.json()
    assert body["mfa_required"] is True
    assert "inventory" in body["allowed_systems"]


def test_erp_invoice_exceptions_endpoint():
    response = client.get("/v1/retail/erp/invoice-exceptions")

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_supply_chain_shipments_endpoint():
    response = client.get("/v1/retail/supply-chain/shipments")

    assert response.status_code == 200
    assert len(response.json()) >= 1
