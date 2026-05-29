#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"

echo "== Health Check =="
curl -s "$BASE_URL/health"
echo
echo

echo "== Risk Tiers =="
curl -s "$BASE_URL/v1/risk/tiers"
echo
echo

echo "== Governance Dashboard =="
curl -s "$BASE_URL/v1/governance/dashboard"
echo
echo

echo "== Retail Systems =="
curl -s "$BASE_URL/v1/retail/systems"
echo
echo

echo "== Inventory Contract =="
curl -s "$BASE_URL/v1/retail/contracts/inventory"
echo
echo

echo "== Run Inventory Replenishment Agent =="
AGENT_RESPONSE="$(curl -s -X POST "$BASE_URL/v1/agents/inventory-replenishment/run" \
  -H "Content-Type: application/json" \
  -d '{"requested_by":"interview-demo","store_ids":["STORE-1042","STORE-2210"]}')"

echo "$AGENT_RESPONSE"
echo
echo

WORKFLOW_ID="$(python3 - <<PY
import json
payload = json.loads('''$AGENT_RESPONSE''')
print(payload["workflow_id"])
PY
)"

echo "Workflow ID: $WORKFLOW_ID"
echo

echo "== Approve Workflow Handoff =="
curl -s -X POST "$BASE_URL/v1/agents/inventory-replenishment/approval" \
  -H "Content-Type: application/json" \
  -d "{
    \"workflow_id\":\"$WORKFLOW_ID\",
    \"approved_by\":\"store-manager-1042\",
    \"decision\":\"approve\",
    \"approval_note\":\"Approved for controlled handoff.\"
  }"
echo
echo

echo "== Policy Gate: Deny Autonomous Purchase Order =="
curl -s -X POST "$BASE_URL/v1/policies/action-gate" \
  -H "Content-Type: application/json" \
  -d '{
    "action_name":"create_purchase_order",
    "retail_system":"Inventory",
    "action_type":"autonomous_execution",
    "risk_tier":"Tier 4",
    "human_approval_status":"approved",
    "mutates_retail_system":true
  }'
echo
echo

echo "== Observability Dashboard =="
curl -s "$BASE_URL/v1/observability/dashboard"
echo
echo

echo "== Expensive Workflow Cost Guardrail =="
curl -s -X POST "$BASE_URL/v1/observability/cost-guardrail" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_id":"wf-expensive",
    "estimated_tokens":12000,
    "estimated_cost_usd":0.12,
    "max_tokens":5000,
    "max_cost_usd":0.05,
    "risk_tier":"Tier 2"
  }'
echo
echo

echo "Demo walkthrough complete."
